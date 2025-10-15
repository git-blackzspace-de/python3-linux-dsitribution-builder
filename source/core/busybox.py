import os
import subprocess
import json
from pathlib import Path
from utils.download import download_file, extract_tarball  # Wir nutzen das vorherige Skript für Download/Extraktion

CONFIG_PATCH = """
# Disable unnecessary features
CONFIG_TOOLS=y
CONFIG_TINYCC=n
"""


def patch_busybox_config(busybox_dir):
    # Erstelle default config
    subprocess.run(["make", "defconfig"], cwd=busybox_dir, check=True)

    config_path = Path(busybox_dir) / ".config"
    # Patch: TC deaktivieren
    with open(config_path, "a") as f:
        f.write(CONFIG_PATCH)

def compile_busybox(busybox_dir, cross_compile, install_dir):
    env = os.environ.copy()
    if cross_compile:
        env["ARCH"] = cross_compile.get("arch", "arm64")
        env["CROSS_COMPILE"] = cross_compile.get("compiler_prefix", "")
        env["CFLAGS"] = cross_compile.get("cflags", "")
        env["LDFLAGS"] = cross_compile.get("ldflags", "")
    
    # Kompilieren
    subprocess.run(["make", "-j4"], cwd=busybox_dir, check=True, env=env)
    
    # Installation in rootfs
    subprocess.run(["make", f"CONFIG_PREFIX={install_dir}", "install"], cwd=busybox_dir, check=True, env=env)

def build_busybox(config):
    
    
    version = config["version"]
    url = config["url"]
    cross_compile = config.get("cross_compile", {})
    output_dir = Path(config.get("output_dir", "build")) / f"busybox-{version}"
    downloads_dir = Path("downloads")
    
    downloads_dir.mkdir(exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filename = downloads_dir / os.path.basename(url)
    
    # Download
    if not filename.exists():
        download_file(url, filename)
    else:
        print(f"{filename} already exists, skipping download.")
    
    # Extract
    print(f"Extracting {filename} to {output_dir}")
    extract_tarball(filename, output_dir)
    
    # Patch BusyBox config
    print("Patching BusyBox .config for ARM64...")
    patch_busybox_config(output_dir)
    
    # Compile & Install
    rootfs_dir = Path("build") / "rootfs"
    rootfs_dir.mkdir(exist_ok=True)
    
    print("Compiling BusyBox for ARM64...")
    compile_busybox(output_dir, cross_compile, rootfs_dir)
    
    print(f"BusyBox successfully compiled and installed in {rootfs_dir}")

# if __name__ == "__main__":
#     main()
