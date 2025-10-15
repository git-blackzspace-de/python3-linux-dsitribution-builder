import os
import sys
import requests
import tarfile


from tqdm import tqdm

def download_file(url, dest):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(dest, 'wb') as f, tqdm(
        desc=f"Downloading {os.path.basename(dest)}",
        total=total,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            f.write(data)
            bar.update(len(data))

def extract_tarball(tar_path, extract_to):
    if tar_path.endswith(".tar.gz") or tar_path.endswith(".tgz"):
        mode = "r:gz"
    elif tar_path.endswith(".tar.bz2"):
        mode = "r:bz2"
    else:
        raise ValueError("Unsupported archive format")
    
    with tarfile.open(tar_path, mode) as tar:
        tar.extractall(path=extract_to)
