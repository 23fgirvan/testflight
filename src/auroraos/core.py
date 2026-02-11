from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class ProcessState(str, Enum):
    NEW = "new"
    RUNNING = "running"
    BACKGROUND = "background"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


@dataclass(slots=True)
class AppManifest:
    bundle_id: str
    name: str
    version: str
    permissions: set[str]
    entrypoint: str


@dataclass(slots=True)
class Process:
    pid: int
    bundle_id: str
    memory_limit_mb: int
    state: ProcessState = ProcessState.NEW
    memory_used_mb: int = 0


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[dict], None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[dict], None]) -> None:
        self._subscribers.setdefault(event_name, []).append(handler)

    def publish(self, event_name: str, payload: dict) -> None:
        for handler in self._subscribers.get(event_name, []):
            handler(payload)


class SecurityManager:
    def __init__(self) -> None:
        self._grants: dict[str, set[str]] = {}

    def grant(self, bundle_id: str, permission: str) -> None:
        self._grants.setdefault(bundle_id, set()).add(permission)

    def enforce_manifest(self, manifest: AppManifest) -> bool:
        granted = self._grants.get(manifest.bundle_id, set())
        return manifest.permissions.issubset(granted)

    def check(self, bundle_id: str, permission: str) -> bool:
        return permission in self._grants.get(bundle_id, set())


class ProcessManager:
    def __init__(self) -> None:
        self._next_pid = 100
        self._table: dict[int, Process] = {}

    def launch(self, bundle_id: str, memory_limit_mb: int = 512) -> Process:
        proc = Process(pid=self._next_pid, bundle_id=bundle_id, memory_limit_mb=memory_limit_mb)
        proc.state = ProcessState.RUNNING
        self._table[proc.pid] = proc
        self._next_pid += 1
        return proc

    def set_background(self, pid: int) -> None:
        self._table[pid].state = ProcessState.BACKGROUND

    def suspend(self, pid: int) -> None:
        self._table[pid].state = ProcessState.SUSPENDED

    def terminate(self, pid: int) -> None:
        self._table[pid].state = ProcessState.TERMINATED

    def running(self) -> list[Process]:
        return [p for p in self._table.values() if p.state in {ProcessState.RUNNING, ProcessState.BACKGROUND}]


@dataclass(slots=True)
class Notification:
    title: str
    body: str
    bundle_id: str


class NotificationCenter:
    def __init__(self) -> None:
        self._inbox: list[Notification] = []

    def send(self, notification: Notification) -> None:
        self._inbox.append(notification)

    def list_inbox(self) -> list[Notification]:
        return list(self._inbox)


@dataclass(slots=True)
class HomeScreen:
    pages: list[list[str]] = field(default_factory=lambda: [[]])
    dock: list[str] = field(default_factory=list)

    def add_app(self, bundle_id: str) -> None:
        last = self.pages[-1]
        if len(last) >= 20:
            self.pages.append([])
            last = self.pages[-1]
        last.append(bundle_id)

    def render(self) -> str:
        lines = ["=== AURORA SPRINGBOARD ==="]
        lines.append(f"Dock: {', '.join(self.dock) if self.dock else '(empty)'}")
        for idx, page in enumerate(self.pages, start=1):
            lines.append(f"Page {idx}: {', '.join(page) if page else '(empty)'}")
        return "\n".join(lines)


class PackageManager:
    def __init__(self) -> None:
        self._apps: dict[str, AppManifest] = {}

    def install(self, manifest: AppManifest) -> None:
        if not manifest.bundle_id or "." not in manifest.bundle_id:
            raise ValueError("invalid bundle id")
        self._apps[manifest.bundle_id] = manifest

    def get(self, bundle_id: str) -> AppManifest:
        return self._apps[bundle_id]

    def all_apps(self) -> list[AppManifest]:
        return list(self._apps.values())


class AuroraOS:
    def __init__(self) -> None:
        self.bus = EventBus()
        self.security = SecurityManager()
        self.processes = ProcessManager()
        self.notifications = NotificationCenter()
        self.packages = PackageManager()
        self.home = HomeScreen(dock=["com.aurora.settings", "com.aurora.browser"])
        self.foreground_pid: int | None = None
        self.bus.subscribe("app_installed", self._on_app_installed)

    def boot(self) -> list[str]:
        return [
            "BootROM: secure boot check passed",
            "Kernel: scheduler online",
            "Launchd: core services initialized",
            "WindowServer: compositor started",
            "Springboard: home screen active",
        ]

    def install_app(self, manifest: AppManifest, auto_grant: bool = False) -> None:
        if auto_grant:
            for perm in manifest.permissions:
                self.security.grant(manifest.bundle_id, perm)
        if not self.security.enforce_manifest(manifest):
            missing = manifest.permissions - self.security._grants.get(manifest.bundle_id, set())
            raise PermissionError(f"install blocked, missing grants: {sorted(missing)}")
        self.packages.install(manifest)
        self.bus.publish("app_installed", {"bundle_id": manifest.bundle_id})

    def launch_app(self, bundle_id: str) -> Process:
        manifest = self.packages.get(bundle_id)
        proc = self.processes.launch(manifest.bundle_id)
        if self.foreground_pid is not None:
            self.processes.set_background(self.foreground_pid)
        self.foreground_pid = proc.pid
        return proc

    def send_notification(self, bundle_id: str, title: str, body: str) -> None:
        if not self.security.check(bundle_id, "notifications"):
            raise PermissionError(f"{bundle_id} missing notifications permission")
        self.notifications.send(Notification(title=title, body=body, bundle_id=bundle_id))

    def _on_app_installed(self, payload: dict) -> None:
        bundle_id = payload["bundle_id"]
        if bundle_id not in self.home.dock:
            self.home.add_app(bundle_id)
