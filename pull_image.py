import os
import tarfile
import urllib.request
import shutil
import sys

# Minimal RootFS sources
DISTROS = {
    "alpine": "https://dl-cdn.alpinelinux.org/alpine/v3.19/releases/x86_64/alpine-minirootfs-3.19.1-x86_64.tar.gz",
    "ubuntu": "https://cdimage.ubuntu.com/ubuntu-base/releases/22.04/release/ubuntu-base-22.04.4-base-amd64.tar.gz",
    "debian": "https://github.com/debuerreotype/docker-debian-artifacts/raw/dist-amd64/bookworm/rootfs.tar.xz"
}

def setup_rootfs(distro_name, target_dir="./rootfs"):
    if distro_name not in DISTROS:
        print(f"Error: Distro '{distro_name}' not supported. Choose from: {list(DISTROS.keys())}")
        return

    # 1. Cleanup old rootfs
    if os.path.exists(target_dir):
        print(f"Cleaning up old {target_dir}...")
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)

    # 2. Download
    url = DISTROS[distro_name]
    file_name = f"base_image.tar.gz"
    print(f"Downloading {distro_name} from {url}...")
    
    try:
        urllib.request.urlretrieve(url, file_name)
        print("Download complete.")

        # 3. Extract
        print(f"Extracting to {target_dir}...")
        with tarfile.open(file_name) as tar:
            tar.extractall(path=target_dir)
        
        print(f"Success! {distro_name} is ready in {target_dir}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 4. Cleanup the tar file
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "alpine"
    setup_rootfs(name)
