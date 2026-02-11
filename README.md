# AuroraOS Tablet (iOS-like) Starter

AuroraOS is a **full-stack starter** for a tablet operating system inspired by modern mobile platforms (like iOS), including:

- A modular kernel simulation
- App sandboxing and permission management
- A compositor/window server model
- Touch-first Springboard-style launcher UX
- Background services, notifications, and package installation

> This repository is a practical blueprint and runnable simulation, not a production kernel. Building a real shipping OS requires years of platform, hardware, security, and compliance work.

## Project layout

- `docs/ARCHITECTURE.md` — system architecture and subsystems
- `docs/ROADMAP.md` — milestones from simulator to hardware bring-up
- `src/auroraos/` — runnable Python implementation of the core platform model

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
auroraos-demo
```

You should see a simulated boot sequence, launcher rendering, app installs, and app lifecycle transitions.

## Why this structure

A realistic tablet OS needs clear separation between:

1. Privileged core services (kernel, process manager, security policy)
2. UI and compositor services (window server, input routing)
3. App runtime and SDK boundary
4. Distribution and updates (package manager / app store channel)

This starter gives you all four so you can iterate toward a real implementation.
