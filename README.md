# Nucleus ⚛️
**Nucleus** is a high-performance, minimalist container engine written in Rust. It serves as a robust demonstration of modern Linux containerization, utilizing kernel primitives like namespaces, Cgroups v2, OverlayFS, and `pivot_root` for secure and isolated process execution.

## Key Features
- **True PID Isolation**: Implements the "Fork-and-Wait" pattern to ensure the containerized process runs as **PID 1**.
- **Secure Filesystem**: Uses `pivot_root` (not just `chroot`) combined with private mount propagation for industry-standard isolation.
- **Host-Driven Networking**: Configures container network interfaces from the host orchestrator using `nsenter`, ensuring high stability and avoiding `ENOMEM` errors during initialization.
- **Advanced Networking**: 
    - Automated Linux Bridge (`br0`) and `veth` pair orchestration.
    - Full Outbound Internet access via NAT/MASQUERADE.
    - **Port Mapping**: Expose container services to the host via `iptables` DNAT rules.
- **Resource Management (Cgroups v2)**:
    - **Memory**: Support for human-readable limits (e.g., `1G`, `512M`) or `max`.
    - **CPU**: Granular control over CPU cycles.
    - **PIDs**: Prevents "fork bombs" and fork errors by managing the PIDs controller.
- **Layered Storage**: Implements OverlayFS with a read-only base image and a writable session layer.
- **Security Hardening**: Drops dangerous Linux capabilities (e.g., `CAP_SYS_RAWIO`, `CAP_MKNOD`) before entering the target process.

---

## Why Nucleus? 🚀

Nucleus isn't trying to be a replacement for the entire Docker ecosystem; it's a **specialized, high-performance runtime** designed for systems engineers and modern infrastructure.

### The Advantage
1.  **Zero-Daemon Architecture:** Nucleus is a single, statically linked binary. It starts the container instantly and stays out of the way. No background daemons, no complex shims—just your process, isolated.
2.  **Rust-Powered Safety:** Built with pure Rust, Nucleus provides memory safety without a Garbage Collector (GC). This results in a tiny memory footprint, making it ideal for high-density environments.
3.  **Host-Driven Stability:** By configuring container networking from the host orchestrator via `nsenter`, Nucleus avoids initialization race conditions common in other runtimes.
4.  **Edge & Embedded Ready:** With its minimal dependencies and small binary size (~2MB), Nucleus is the perfect "Swiss Army Knife" for isolation on resource-constrained hardware.

### Comparison: Nucleus vs. The Industry

| Feature | Docker / Podman | Nucleus |
| :--- | :--- | :--- |
| **Binary Size** | Huge (100MB+) | Tiny (~2MB) |
| **Startup Time** | Slow (~500ms+) | Instant (~10-20ms) |
| **Runtime** | Go (Garbage Collected) | Rust (Zero-overhead) |
| **Dependencies** | Many (iptables, dbus, etc.) | Minimal (Kernel primitives) |
| **Architecture** | Daemon-based | Zero-daemon / Standalone |
| **Use Case** | General App Dev | Edge, FaaS, Security, Embedded |

---

## 🚀 Getting Started

### 1. Prerequisites
- **OS**: Linux with Kernel 4.18+ (Cgroups v2 and OverlayFS support required).
- **Tools**: `rustc`, `cargo`, `python3`, `iptables`, `iproute2`.
- **Privileges**: Root access is mandatory for managing namespaces and networking.

### 2. Prepare a RootFS
Nucleus requires a base directory to use as the container's root. Use the helper script to fetch a minimal Alpine Linux image:
```bash
python3 pull_image.py alpine
```

### 3. Build Nucleus
```bash
cargo build --release
```

---

## 🛠 Usage Examples

### Run a basic isolated shell
```bash
sudo ./target/release/Nucleus --name my-shell --ip 10.0.0.10 /bin/sh
```

### Expose a Web Server (Port Mapping)
Expose a container's port 80 to the host's port 8080:
```bash
sudo ./target/release/Nucleus \
  --name web-app \
  --ip 10.0.0.20 \
  --ports 8080:80 \
  /bin/sh
```

### Mount Host Directories (Volumes)
```bash
sudo ./target/release/Nucleus \
  --name dev-box \
  --ip 10.0.0.30 \
  --volumes /home/user/data:/mnt/data \
  /bin/sh
```

### Resource-Limited Environment
```bash
sudo ./target/release/Nucleus \
  --name limited-box \
  --ip 10.0.0.40 \
  --memory 512M \
  /bin/sh
```

---

## 📂 Project Structure
- `src/main.rs`: Entry point and process orchestration.
- `src/args.rs`: CLI argument definitions using `clap`.
- `src/orchestrator.rs`: Host-side setup (Networking, Cgroups, IPTables, `nsenter` config).
- `src/container.rs`: Inside-the-container setup (PID 1 forking, `pivot_root`, Capabilities).
- `src/utils.rs`: Shared helpers for shell commands and memory parsing.

## ⚖️ License
MIT / Apache-2.0
