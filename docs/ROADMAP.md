# AuroraOS Roadmap

## Phase 0 — Prototype (current)

- [x] Boot sequence simulator
- [x] Process + scheduler model
- [x] App install and permission checks
- [x] Launcher and app switching simulation

## Phase 1 — SDK + tooling

- [ ] Public SDK for third-party apps
- [ ] Emulator CLI and snapshot support
- [ ] App signing CLI and cert management
- [ ] Automated compatibility tests

## Phase 2 — Native runtime

- [ ] Replace Python services with Rust daemons
- [ ] Build IPC system (capability based)
- [ ] Persistent storage and journaling FS
- [ ] GPU-accelerated rendering

## Phase 3 — Device bring-up

- [ ] Board support package for selected tablet SoC
- [ ] Secure boot, TPM/SE integration
- [ ] Power management and thermal controls
- [ ] Camera/audio/touch sensor pipelines

## Phase 4 — Platform hardening

- [ ] Verified boot + attestation
- [ ] Full sandbox + exploit mitigations
- [ ] Accessibility, localization, parental controls
- [ ] Store/review pipeline
