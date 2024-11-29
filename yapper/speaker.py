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
    get_random_name,
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
    # Mapping of voices to their highest supported quality
    VOICE_QUALITY_MAP = {
        PiperVoice.ARCTIC: PiperQuality.MEDIUM,
        PiperVoice.BRYCE: PiperQuality.MEDIUM,
        PiperVoice.DANNY: PiperQuality.LOW,
        PiperVoice.HFC_FEMALE: PiperQuality.MEDIUM,
        PiperVoice.HFC_MALE: PiperQuality.MEDIUM,
        PiperVoice.JOE: PiperQuality.MEDIUM,
        PiperVoice.JOHN: PiperQuality.MEDIUM,
        PiperVoice.KATHLEEN: PiperQuality.LOW,
        PiperVoice.KRISTIN: PiperQuality.MEDIUM,
        PiperVoice.KUSAL: PiperQuality.MEDIUM,
        PiperVoice.L2ARCTIC: PiperQuality.MEDIUM,
        PiperVoice.LESSAC: PiperQuality.HIGH,
        PiperVoice.LIBRITTS: PiperQuality.HIGH,
        PiperVoice.LIBRITTS_R: PiperQuality.MEDIUM,
        PiperVoice.LJSPEECH: PiperQuality.HIGH,
        PiperVoice.NORMAN: PiperQuality.MEDIUM,
        PiperVoice.RYAN: PiperQuality.HIGH,
    }

    def __init__(
        self,
        voice: PiperVoice = PiperVoice.AMY,
        quality: PiperQuality = None,
    ):
        """
        Speaks the text using piper.

        Parameters
        ----------
        voice : PiperVoice, optional
            Name of the piper voice to be used, can be one of 'PiperVoice'
            enum's attributes (default: PiperVoice.AMY).
        quality : PiperQuality, optional
            Quality of the voice. If not provided, defaults to the highest
            supported quality for the selected voice.
        """
        assert (
            voice in PiperVoice
        ), f"voice must be one of {', '.join(PiperVoice)}"
        
        # Determine the highest supported quality if none is provided
        self.quality = quality or self.VOICE_QUALITY_MAP[voice]
        assert (
            self.quality in PiperQuality
        ), f"quality must be one of {', '.join(PiperQuality)}"
        
        install_piper()
        self.exe_path = str(
            APP_DIR
            / "piper"
            / ("piper.exe" if PLATFORM == c.PLATFORM_WINDOWS else "piper")
        )
        self.onnx_f, self.conf_f = download_piper_model(
            voice.value, self.quality.value
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

    def save(self, text: str, filename: str):
        """
        Saves the generated audio to a file.

        Parameters
        ----------
        text : str
            The text to convert to speech.
        filename : str
            The path of the file to save the audio.
        """
        subprocess.run(
            [
                self.exe_path,
                "-m",
                self.onnx_f,
                "-c",
                self.conf_f,
                "-f",
                filename,
                "-q",
            ],
            input=text.encode("utf-8"),
            check=True,
            stdout=subprocess.DEVNULL,
        )
