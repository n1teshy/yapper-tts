import os
import subprocess
from abc import ABC, abstractmethod
from typing import Optional

import pyttsx3 as tts

import yapper.constants as c
from yapper.enums import PiperQuality, PiperVoice, PiperVoiceUS
from yapper.utils import (
    APP_DIR,
    download_piper_model,
    get_random_name,
    install_piper,
)

# suppresses pygame's welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame  # noqa: E402


def play_wave(wave_f: str, volume: float = 1.0):
    """
    Plays the given wave file using pygame.

    Parameters
    ----------
    wave_f : str
        The wave file to play.
    volume : float, optional
        Volume to play the wave file between 0.0 and 1.0 (default: 1.0)
    """
    pygame.mixer.init()  # initialize pygame, safe to call multiple times
    sound = pygame.mixer.Sound(wave_f)
    sound.set_volume(volume)  # sets volume, defaults to 1

    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.wait(100)


class BaseSpeaker(ABC):
    """
    Base class for speakers

    Methods
    ----------
    say(text: str)
        Speaks the given text.
    text_to_wave(text: str, file: str)
        Speaks the given text, saves the speech to a wave file.
    """

    @abstractmethod
    def say(self, text: str):
        pass

    @abstractmethod
    def text_to_wave(self, text: str, file: str):
        pass


class PyTTSXSpeaker(BaseSpeaker):
    """Converts speech to text using pyttsx."""

    def __init__(
        self,
        voice: str = c.VOICE_FEMALE,
        rate: int = c.SPEECH_RATE,
        volume: str = c.SPEECH_VOLUME,
    ):
        """
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

    def text_to_wave(self, text: str, file: str):
        """Saves the speech for the given text into the given file."""
        engine = tts.init()
        engine.setProperty("rate", self.rate)
        engine.setProperty("volume", self.volume)
        voice_id = engine.getProperty("voices")[
            int(self.voice == c.VOICE_FEMALE)
        ].id
        engine.setProperty("voice", voice_id)
        engine.save_to_file(text, file)
        engine.runAndWait()

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
    """Converts text to speech using piper-tts"""

    def __init__(
        self,
        voice: PiperVoice = PiperVoiceUS.HFC_FEMALE,
        quality: Optional[PiperQuality] = None,
        show_progress: bool = True,
        volume: float = 1.0,
    ):
        """
        Parameters
        ----------
        voice : PiperVoice, optional
            Name of the piper voice to be used, can be one of PiperVoice*
            enums's attributes (default: PiperVoiceUS.AMY).
        quality : PiperQuality, optional
            Quality of the voice, can be ont of 'PiperQuality'
            enum's attributes (default: the highest available quality of
            the given voice).
        show_progress : bool
            Show progress when the voice model is being downloaded
            (default: True).
        volume : float, optional
            volume to play the wav file at, between 0.0 and 1.0
            (defaults to 1.0)
        """
        assert isinstance(
            voice, tuple(c.piper_enum_to_lang_code.keys())
        ), "voice must be a member of PiperVoice* enums"
        quality = quality or c.piper_voice_quality_map[voice]
        assert quality in PiperQuality, "quality must a member of PiperQuality"

        self.exe_path = str(install_piper(show_progress))
        self.onnx_f, self.conf_f = download_piper_model(
            voice, quality, show_progress
        )
        self.onnx_f, self.conf_f = str(self.onnx_f), str(self.conf_f)

        self.volume = volume

    def text_to_wave(self, text: str, file: str):
        """Saves the speech for the given text into the given file."""
        subprocess.run(
            [
                self.exe_path,
                "-m",
                self.onnx_f,
                "-c",
                self.conf_f,
                "-f",
                file,
                "-q",
            ],
            input=text.encode("utf-8"),
            stdout=subprocess.DEVNULL,
            check=True,
        )

    def say(self, text: str):
        """Speaks the given text"""
        f = APP_DIR / f"{get_random_name()}.wav"
        try:
            self.text_to_wave(text, str(f))
            play_wave(str(f), self.volume)
        finally:
            if f.exists():
                os.remove(f)
