import json
import os

from utils.download import download_file, extract_tarball
from utils.load import load_config
from utils.create import create_directories, create_etc_files, create_dev_nodes, create_busybox_init

from core.busybox import build_busybox

# --- Funktionen ---




def main():
    config = load_config()
    
    version = config["version"]
    url = config["url"]
    cross_compile = config.get("cross_compile", {})
    output_dir = os.path.join(config.get("output_dir", "build"), f"busybox-{version}")
    
    os.makedirs("downloads", exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    filename = os.path.join("downloads", os.path.basename(url))
    
    create_directories()
    create_etc_files()
    create_dev_nodes()
    create_busybox_init()
    print("Rootfs setup complete.")
    
    build_busybox(config)
    
    
    # Download
        
    

if __name__ == "__main__":
    main()
