import os
import platform
import random
import string
import sys
import tarfile
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

import yapper.constants as c
import yapper.meta as meta
from yapper.enums import PiperQuality, PiperVoiceUK, PiperVoiceUS

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


def get_random_name(length: int = 10) -> str:
    """
    Creates a 'length' letter random string.

    Parameters
    ----------
    length : int, optional
        Length of the random string (default: 10).
    """
    return "".join(random.choices(string.ascii_letters, k=length))


def progress_hook(block_idx: int, block_size: int, total_bytes: int):
    """Shows download progress."""
    part = min(((block_idx + 1) * block_size) / total_bytes, 1)
    progress = "=" * int(60 * part)
    padding = " " * (60 - len(progress))
    print("\r|" + progress + padding + "|", end="")


def download(url: str, file: str, show_progress: bool = True):
    """
    Downloads the content from the given URL into the given file.

    Parameters
    ----------
    url : str
        The URL to download content from.
    file : str
        The file to save the URL content into.
    show_progress: bool, optional
        Whether to show progress while downloading.
    """
    hook = progress_hook if show_progress else None
    urlretrieve(url, file, reporthook=hook)
    print("")


def install_piper():
    """Installs piper into the app's home directory."""
    if (APP_DIR / "piper").exists():
        return
    zip_path = APP_DIR / "piper.zip"
    print("installing piper...")
    prefix = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2"
    if PLATFORM == c.PLATFORM_LINUX:
        if platform.machine() in ("aarch64", "arm64"):
            nix_link = f"{prefix}/piper_linux_aarch64.tar.gz"
        elif platform.machine() in ("armv7l", "armv7"):
            nix_link = f"{prefix}/piper_linux_armv7l.tar.gz"
        else:
            nix_link = f"{prefix}/piper_linux_x86_64.tar.gz"
        download(nix_link, zip_path)
    elif PLATFORM == c.PLATFORM_WINDOWS:
        download(f"{prefix}/piper_windows_amd64.zip", zip_path)
    else:
        download(f"{prefix}/piper_macos_x64.tar.gz", zip_path)

    if PLATFORM == c.PLATFORM_WINDOWS:
        with zipfile.ZipFile(zip_path, "r") as z_f:
            z_f.extractall(APP_DIR)
    else:
        with tarfile.open(zip_path, "r") as z_f:
            z_f.extractall(APP_DIR)
    os.remove(zip_path)


def download_piper_model(
    voice: PiperVoiceUS | PiperVoiceUK, quality: PiperQuality
) -> tuple[str, str]:
    """
    Downloads the given piper voice with the given quality.

    Parameters
    ----------
    voice : PiperVoiceUS or PiperVoiceUK
        The Piper voice model to download.
    quality : PiperQuality
        The quality of the given voice.

    Returns
    ----------
    tuple of str
        The voice model file and the voice configuration file in a tuple.
    """
    voices_dir = APP_DIR / "piper_voices"
    voices_dir.mkdir(exist_ok=True)
    lang_code = "en_US" if isinstance(voice, PiperVoiceUS) else "en_GB"
    voice, quality = voice.value, quality.value

    onnx_file = voices_dir / f"{lang_code}-{voice}-{quality}.onnx"
    conf_file = voices_dir / f"{lang_code}-{voice}-{quality}.onnx.json"

    prefix = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/"
    prefix += lang_code
    help_url = "https://huggingface.co/rhasspy/piper-voices/tree/main/en/"
    help_url += lang_code
    if not onnx_file.exists():
        try:
            print(f"downloading requirements for {voice}...")
            onnx_url = (
                f"{prefix}/{voice}/{quality}/{onnx_file.name}?download=true"
            )
            download(onnx_url, onnx_file)
        except (KeyboardInterrupt, Exception) as e:
            onnx_file.unlink(missing_ok=True)
            if getattr(e, "status", None) == 404:
                raise Exception(
                    f"{voice}({quality}) is not available, please refer to"
                    f" {help_url} to check all available models"
                )
            raise e
    if not conf_file.exists():
        conf_url = f"{prefix}/{voice}/{quality}/{conf_file.name}?download=true"
        try:
            download(conf_url, conf_file)
        except (KeyboardInterrupt, Exception) as e:
            conf_file.unlink(missing_ok=True)
            raise e

    return str(onnx_file), str(conf_file)
