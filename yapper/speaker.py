import os
import subprocess
import wave
from abc import ABC, abstractmethod
from typing import Optional

import pyaudio
import pyttsx3 as tts

import yapper.constants as c
from yapper.enums import PiperQuality, PiperVoice
from yapper.utils import (
    APP_DIR,
    PLATFORM,
    download_piper_model,
    get_random_name,
    install_piper
)


def play_wave(pa_instance: pyaudio.PyAudio, wave_f: str):
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
    VOICE_QUALITY_MAP = {
        PiperVoice.AMY: PiperQuality.MEDIUM,
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
        quality: Optional[PiperQuality] = None,
    ):
        """
        Speaks the text using piper.

        Parameters
        ----------
        voice : PiperVoice, optional
            Name of the piper voice to be used, can be one of 'PiperVoice'
            enum's attributes (default: PiperVoice.AMY).
        quality : PiperQuality, optional
            Quality of the voice, can be ont of 'PiperQuality'
            enum's attributes (default: the highest available quality of
            the given voice).
        """
        assert (
            voice in PiperVoice
        ), f"voice must be one of {', '.join(PiperVoice)}"
        quality = quality or PiperSpeaker.VOICE_QUALITY_MAP[voice]
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
