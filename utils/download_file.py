import subprocess
import os
from utils.decorators import timer_dec


@timer_dec(message="[DONE] Downloaded file")
def download_file(url, output_path):
    print(f"[INFO] Downloading file from {url} to {output_path}")
    dest_file = os.path.join(output_path, os.path.basename(url))
    if not os.path.exists(dest_file):
        cmd = ["wget", url, "-O", dest_file]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    return dest_file