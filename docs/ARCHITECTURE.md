# AuroraOS Architecture

## 1. Kernel layer (simulated)

- Cooperative scheduler (`scheduler.py`)
- Memory manager with per-process soft limits (`memory.py`)
- Process table and lifecycle states (`process.py`)
- Event bus used by privileged services (`event_bus.py`)

## 2. System services

- Security daemon enforcing app permissions and sandbox policy (`security.py`)
- Package manager installing signed app manifests (`package_manager.py`)
- Notification daemon delivering push/local events (`notifications.py`)
- Session manager driving login/lock/foreground policy (`session.py`)

## 3. UI stack

- Compositor / scene graph abstraction (`compositor.py`)
- Springboard-style launcher with dock and home pages (`springboard.py`)
- Touch dispatch and gesture to intent mapping (`input.py`)

## 4. App model

Apps are declarative packages with:

- `bundle_id`
- version and display metadata
- required permissions
- entrypoint callback name

Apps run in isolated process objects and communicate through mediated APIs.

## 5. Security model

- Deny-by-default permissions
- Explicit grants for camera/mic/location/network/notifications
- Install-time signature check (stubbed in simulator)
- Runtime policy checks before service invocation

## 6. Productionization path

To move from simulation to real OS:

1. Replace simulated kernel with a Rust/C microkernel or hardened Linux base
2. Implement hardware abstraction (display, GPU, audio, touch, sensors)
3. Build a native compositor (Wayland-like protocol or custom)
4. Replace package signer stub with PKI and secure boot chain
5. Add OTA update engine with A/B rollback
