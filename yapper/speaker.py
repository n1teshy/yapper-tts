import os
import subprocess
import wave
from abc import ABC, abstractmethod
from typing import Optional

import pyaudio
import pyttsx3 as tts

import yapper.constants as c
from yapper.enums import PiperQuality, PiperVoiceUK, PiperVoiceUS
from yapper.utils import (APP_DIR, PLATFORM, download_piper_model,
                          get_random_name, install_piper)


def play_wave(pa_instance: pyaudio.PyAudio, wave_f: str):
    """
    Plays the given wave file using the given pyaudio.PyAudio instance.

    Parameters
    ----------
    pa_instance : pyaudio.PyAudio
        Gender of the voice, can be 'f' or 'm' (default: 'f').
    wave_f : str
        The wave file to play.
    """
    with wave.open(wave_f, "rb") as wf:
        stream = pa_instance.open(
            format=pa_instance.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True,
        )
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)
        stream.stop_stream()
        stream.close()


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

    VOICE_QUALITY_MAP = {
        PiperVoiceUS.AMY: PiperQuality.MEDIUM,
        PiperVoiceUS.ARCTIC: PiperQuality.MEDIUM,
        PiperVoiceUS.BRYCE: PiperQuality.MEDIUM,
        PiperVoiceUS.DANNY: PiperQuality.LOW,
        PiperVoiceUS.HFC_FEMALE: PiperQuality.MEDIUM,
        PiperVoiceUS.HFC_MALE: PiperQuality.MEDIUM,
        PiperVoiceUS.JOE: PiperQuality.MEDIUM,
        PiperVoiceUS.JOHN: PiperQuality.MEDIUM,
        PiperVoiceUS.KATHLEEN: PiperQuality.LOW,
        PiperVoiceUS.KRISTIN: PiperQuality.MEDIUM,
        PiperVoiceUS.KUSAL: PiperQuality.MEDIUM,
        PiperVoiceUS.L2ARCTIC: PiperQuality.MEDIUM,
        PiperVoiceUS.LESSAC: PiperQuality.HIGH,
        PiperVoiceUS.LIBRITTS: PiperQuality.HIGH,
        PiperVoiceUS.LIBRITTS_R: PiperQuality.MEDIUM,
        PiperVoiceUS.LJSPEECH: PiperQuality.HIGH,
        PiperVoiceUS.NORMAN: PiperQuality.MEDIUM,
        PiperVoiceUS.RYAN: PiperQuality.HIGH,
        PiperVoiceUK.ALAN: PiperQuality.MEDIUM,
        PiperVoiceUK.ALBA: PiperQuality.MEDIUM,
        PiperVoiceUK.ARU: PiperQuality.MEDIUM,
        PiperVoiceUK.CORI: PiperQuality.HIGH,
        PiperVoiceUK.JENNY_DIOCO: PiperQuality.MEDIUM,
        PiperVoiceUK.NORTHERN_ENGLISH_MALE: PiperQuality.MEDIUM,
        PiperVoiceUK.SEMAINE: PiperQuality.MEDIUM,
        PiperVoiceUK.SOUTHERN_ENGLISH_FEMALE: PiperQuality.LOW,
        PiperVoiceUK.VCTK: PiperQuality.MEDIUM,
    }

    def __init__(
        self,
        voice: PiperVoiceUS | PiperVoiceUK = PiperVoiceUS.HFC_FEMALE,
        quality: Optional[PiperQuality] = None,
    ):
        """
        Parameters
        ----------
        voice : PiperVoiceUS, optional
            Name of the piper voice to be used, can be one of 'PiperVoiceUS'
            enum's attributes (default: PiperVoiceUS.AMY).
        quality : PiperQuality, optional
            Quality of the voice, can be ont of 'PiperQuality'
            enum's attributes (default: the highest available quality of
            the given voice).
        """
        assert isinstance(
            voice, (PiperVoiceUS, PiperVoiceUK)
        ), "voice must be a member of PiperVoiceUS or PiperVoiceUK"
        quality = quality or PiperSpeaker.VOICE_QUALITY_MAP[voice]
        assert (
            quality in PiperQuality
        ), "quality must a member of PiperQuality"
        install_piper()
        self.exe_path = str(
            APP_DIR
            / "piper"
            / ("piper.exe" if PLATFORM == c.PLATFORM_WINDOWS else "piper")
        )
        self.onnx_f, self.conf_f = download_piper_model(voice, quality)
        self.onnx_f, self.conf_f = str(self.onnx_f), str(self.conf_f)
        self.pa_instance = pyaudio.PyAudio()

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
            play_wave(self.pa_instance, str(f))
        finally:
            if f.exists():
                os.remove(f)
