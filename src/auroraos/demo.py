from auroraos.core import AppManifest, AuroraOS


def main() -> None:
    os = AuroraOS()

    print("\n".join(os.boot()))
    print()

    notes_app = AppManifest(
        bundle_id="com.example.notes",
        name="Notes Pro",
        version="1.0.0",
        permissions={"notifications", "storage"},
        entrypoint="notes.main",
    )

    maps_app = AppManifest(
        bundle_id="com.example.maps",
        name="CityMaps",
        version="1.0.0",
        permissions={"location", "network", "notifications"},
        entrypoint="maps.main",
    )

    os.install_app(notes_app, auto_grant=True)
    os.install_app(maps_app, auto_grant=True)

    notes_proc = os.launch_app("com.example.notes")
    maps_proc = os.launch_app("com.example.maps")

    os.send_notification("com.example.notes", "Sync complete", "Your notes are up to date.")
    os.send_notification("com.example.maps", "Traffic alert", "Heavy traffic on Market Street.")

    print(os.home.render())
    print()
    print(f"Foreground PID: {os.foreground_pid}")
    print(f"Running processes: {[p.pid for p in os.processes.running()]}")
    print(f"Last launched app PID: {maps_proc.pid}, previous: {notes_proc.pid}")

    print("\n=== NOTIFICATION CENTER ===")
    for item in os.notifications.list_inbox():
        print(f"[{item.bundle_id}] {item.title} — {item.body}")


if __name__ == "__main__":
    main()
