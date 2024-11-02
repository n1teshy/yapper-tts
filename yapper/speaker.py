import os
import subprocess
from abc import ABC, abstractmethod

import pyttsx3 as tts

import yapper.constants as c
from yapper.enums import PiperQuality, PiperVoice
from yapper.utils import (
    APP_DIR,
    PLATFORM,
    install_piper,
    download_piper_model,
    get_random_name
)

# suppresses pygame's welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame  # noqa: E402


class BaseSpeaker(ABC):
    """
    Base class for speakers

    Methods
    ----------
    say(text: str)
        Speaks the given text.
    """

    @abstractmethod
    def say(self, text: str):
        pass


class DefaultSpeaker(BaseSpeaker):
    def __init__(
        self,
        voice: str = c.VOICE_FEMALE,
        rate: int = c.SPEECH_RATE,
        volume: str = c.SPEECH_VOLUME,
    ):
        """
        Speaks the text using pyttsx.

        Parameters
        ----------
        voice : str, optional
            Gender of the voice, can be 'f' or 'm' (default: 'f').
        rate : int, optional
            Rate of speech of the voice in wpm (default: 165).
        volume : float, optional
            Volume of the sound generated, can be 0-1 (default: 1).
        """
        assert voice in (
            c.VOICE_MALE,
            c.VOICE_FEMALE,
        ), "unknown voice requested"
        self.voice = voice
        self.rate = rate
        self.volume = volume

    def say(self, text: str):
        """Speaks the given text"""
        engine = tts.init()
        engine.setProperty("rate", self.rate)
        engine.setProperty("volume", self.volume)
        voice_id = engine.getProperty("voices")[
            int(self.voice == c.VOICE_FEMALE)
        ].id
        engine.setProperty("voice", voice_id)
        engine.say(text)
        engine.runAndWait()


class PiperSpeaker(BaseSpeaker):
    def __init__(
        self,
        voice: PiperVoice = PiperVoice.AMY,
        quality: PiperQuality = PiperQuality.MEDIUM,
    ):
        """
        Speaks the text using piper.

        Parameters
        ----------
        voice : str, optional
            Name of the piper voice to be used, can be one of 'PiperVoice'
            enum's attributes (default: PiperVoice.AMY).
        quality : str, optional
            Quality of the voice, can be ont of 'PiperQuality'
            enum's attributes (default: PiperQuality.MEDIUM).
        """
        assert (
            voice in PiperVoice
        ), f"voice must be one of {', '.join(PiperVoice)}"
        assert (
            quality in PiperQuality
        ), f"quality must be one of {', '.join(PiperQuality)}"
        install_piper()
        self.exe_path = str(
            APP_DIR
            / "piper"
            / ("piper.exe" if PLATFORM == c.PLATFORM_WINDOWS else "piper")
        )
        self.onnx_f, self.conf_f = download_piper_model(
            voice.value, quality.value
        )
        self.onnx_f, self.conf_f = str(self.onnx_f), str(self.conf_f)
        pygame.mixer.init()

    def say(self, text: str):
        """Speaks the given text"""
        f = APP_DIR / f"{get_random_name()}.wav"
        subprocess.run(
            [
                self.exe_path,
                "-m",
                self.onnx_f,
                "-c",
                self.conf_f,
                "-f",
                str(f),
                "-q",
            ],
            input=text.encode("utf-8"),
            check=True,
            stdout=subprocess.DEVNULL,
        )
        sound = pygame.mixer.Sound(f)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.wait(100)
        os.remove(f)
