import os
import random
import string
import sys
import tarfile
import zipfile
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlretrieve

import yapper.constants as c
import yapper.meta as meta

PLATFORM = None
APP_DIR = None

if os.name == "nt":
    PLATFORM = c.PLATFORM_WINDOWS
    APP_DIR = Path(os.getenv("APPDATA"))
elif os.name == "posix":
    home = Path.home()
    if os.uname().sysname == "Darwin":
        PLATFORM = c.PLATFORM_MAC
        APP_DIR = Path.home() / "Library/Application Support"
    else:
        PLATFORM = c.PLATFORM_LINUX
        APP_DIR = Path.home() / ".config"
else:
    print("your system is not supported")
    sys.exit()

APP_DIR = APP_DIR / meta.name
APP_DIR.mkdir(exist_ok=True)


def get_random_name(length=10):
    return "".join(random.choices(string.ascii_letters, k=length))


def progress_hook(block_idx, block_size, total_bytes):
    part = min(((block_idx + 1) * block_size) / total_bytes, 1)
    progress = "=" * int(60 * part)
    padding = " " * (60 - len(progress))
    print("\r|" + progress + padding + "|", end="")


def download(url, file):
    urlretrieve(url, file, reporthook=progress_hook)
    print("")


def install_piper():
    if (APP_DIR / "piper").exists():
        return
    zip_path = APP_DIR / "piper.zip"
    print("installing piper...")
    prefix = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2"
    nt_link = f"{prefix}/piper_windows_amd64.zip"
    nix_link = f"{prefix}/piper_linux_x86_64.tar.gz"
    mac_link = f"{prefix}/piper_macos_x64.tar.gz"
    if PLATFORM == c.PLATFORM_WINDOWS:
        download(nt_link, zip_path)
    elif PLATFORM == c.PLATFORM_LINUX:
        download(nix_link, zip_path)
    else:
        download(mac_link, zip_path)
    if PLATFORM == c.PLATFORM_WINDOWS:
        with zipfile.ZipFile(zip_path, "r") as z_f:
            z_f.extractall(APP_DIR)
    else:
        with tarfile.open(zip_path, "r") as z_f:
            z_f.extractall(APP_DIR)
    os.remove(zip_path)


def download_piper_model(voice, quality):
    voices_dir = APP_DIR / "piper_voices"
    voices_dir.mkdir(exist_ok=True)
    onnx_file = voices_dir / f"en_US-{voice}-{quality}.onnx"
    conf_file = voices_dir / f"en_US-{voice}-{quality}.onnx.json"
    prefix = (
        "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US"
    )
    help_url = "https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US"
    if not onnx_file.exists():
        try:
            print(f"downloading requirements for {voice}...")
            onnx_url = (
                f"{prefix}/{voice}/{quality}/{onnx_file.name}?download=true"
            )
            download(onnx_url, onnx_file)
        except HTTPError as e:
            if hasattr(e, "status") and e.status == 404:
                raise Exception(
                    f"{voice}({quality}) is not available, please refer to"
                    f" {help_url} to check all available models"
                )
            raise e
    if not conf_file.exists():
        conf_url = f"{prefix}/{voice}/{quality}/{conf_file.name}?download=true"
        download(conf_url, conf_file)

    return onnx_file, conf_file
