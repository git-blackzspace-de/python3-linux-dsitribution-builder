import os
from pathlib import Path
import stat

# Basisverzeichnisse
app_dir = Path(__file__).parent.resolve()
downloads_dir = app_dir / "downloads"
build_dir = app_dir / "build"
rootfs_dir = build_dir / "rootfs"
bootfs_dir = build_dir / "bootfs"

# Linux rootfs typische Verzeichnisse
rootfs_subdirs = [
    "bin",
    "sbin",
    "etc",
    "proc",
    "sys",
    "dev",
    "tmp",
    "var",
    "usr/bin",
    "usr/sbin",
    "home",
    "root",
    "lib",
    "lib64",
    "mnt",
    "media",
]

# Minimal /etc config files
etc_files = {
    "fstab": "proc /proc proc defaults 0 0\n",
    "hostname": "mydevice\n",
    "hosts": "127.0.0.1 localhost\n",
    "inittab": "::sysinit:/etc/init.d/rcS\n",
}

# Device nodes zu simulieren (echte Device Nodes erfordern Rootrechte)
dev_nodes = [
    "null",
    "zero",
    "console",
    "tty",
]

# BusyBox init system
init_script_content = """#!/bin/sh
echo "Starting minimal BusyBox init..."
mount -t proc none /proc
mount -t sysfs none /sys
echo "Root filesystem ready."
exec /bin/sh
"""

def create_directories():
    print("Creating main directories...")
    for d in [downloads_dir, build_dir, rootfs_dir, bootfs_dir]:
        d.mkdir(parents=True, exist_ok=True)
        print(f"Created {d}")

    print("Creating rootfs directories...")
    for sub in rootfs_subdirs:
        path = rootfs_dir / sub
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created {path}")

def create_etc_files():
    etc_path = rootfs_dir / "etc"
    print("Creating /etc configuration files...")
    for filename, content in etc_files.items():
        file_path = etc_path / filename
        file_path.write_text(content)
        print(f"Created {file_path}")

def create_dev_nodes():
    dev_path = rootfs_dir / "dev"
    print("Simulating device nodes...")
    for node in dev_nodes:
        node_path = dev_path / node
        node_path.touch(exist_ok=True)
        # Set dummy permissions (like actual devices)
        node_path.chmod(stat.S_IFCHR | 0o666)  # char device, rw-rw-rw-
        print(f"Created simulated device node {node_path}")

def create_busybox_init():
    init_path = rootfs_dir / "init"
    init_path.write_text(init_script_content)
    init_path.chmod(0o755)
    print(f"Created BusyBox init script at {init_path}")

# if __name__ == "__main__":
#     create_directories()
#     create_etc_files()
#     create_dev_nodes()
#     create_busybox_init()
#     print("Rootfs setup complete.")
