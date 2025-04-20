import json
from abc import ABC, abstractmethod
from typing import Optional
from urllib.request import Request, urlopen

import yapper.constants as c
from yapper.enums import GeminiModel, GroqModel, Persona


def enhancer_gemini(
    model: str, persona_instr: str, api_key: str, text: str
) -> str:
    """
    Enhances the given text using Gemini.

    Parameters
    ----------
    model : str
        The gemini model to use for enhancing text.
    persona_instr : the persona instruction to use for text enhancement,
        can be any system message.
    api_key : str
        The Gemini API key used for making request.
    query: str
        The text to enhance.
    """
    base = "https://generativelanguage.googleapis.com/v1beta/models"
    url = f"{base}/{model}:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        c.GEMINI_FLD_SYS_INST: {
            c.GEMINI_FLD_PARTS: {c.GEMINI_FLD_TEXT: persona_instr}
        },
        c.GEMINI_FLD_CONTENTS: {c.GEMINI_FLD_PARTS: {c.GEMINI_FLD_TEXT: text}},
    }
    request = Request(
        url, headers=headers, data=json.dumps(data).encode("utf-8")
    )
    with urlopen(request) as response:
        data = json.loads(response.read())
        return data[c.GEMINI_FLD_CANDIDATES][0][c.GEMINI_FLD_CONTENT][
            c.GEMINI_FLD_PARTS
        ][0][c.GEMINI_FLD_TEXT]


def enhancer_groq(
    model: str, api_key: str, persona_instr: str, text: str
) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "curl/7.68.0",
    }
    data = {
        c.GROQ_FLD_MESSAGES: [
            {c.FLD_ROLE: c.ROLE_SYSTEM, c.FLD_CONTENT: persona_instr},
            {c.FLD_ROLE: c.ROLE_USER, c.FLD_CONTENT: text},
        ],
        c.GROQ_FLD_MODEL: model,
    }
    with urlopen(
        Request(url, headers=headers, data=json.dumps(data).encode("utf-8"))
    ) as response:
        data = json.loads(response.read())
        return data[c.FLD_CHOICES][0][c.FLD_MESSAGE][c.FLD_CONTENT]


class BaseEnhancer(ABC):
    """
    Base class for text enhancers.

    Methods
    ----------
    enhance(text: str) -> str
        Enhances the given text.
    """

    @abstractmethod
    def enhance(self, text: str) -> str:
        pass


class NoEnhancer(BaseEnhancer):
    """Doesn't do anything to the text, a placeholder for a real enhancer."""

    def enhance(self, text: str):
        return text


class GeminiEnhancer(BaseEnhancer):
    """Enhances text using a Gemini model."""

    def __init__(
        self,
        api_key: str,
        model: GeminiModel = GeminiModel.GEMINI_1_5_PRO,
        persona: Persona = Persona.DEFAULT,
        persona_instr: Optional[str] = None,
    ):
        """
        Parameters
        ----------
        api_key : str
            Your gemini api key.
        gemini_model : GeminiModel, optional
            the gemini model to use for enhancement, must be one of
            'GeminiModel' enum's attributes
            (default: GeminiModel.PRO_1_5_002).
        persona : Persona, optional
            The persona to be used for enhancement (default: Persona.DEFAULT).
        persona_instr : Optional[str]
            Custom persona instruction, can be used to give the LLM a custom
            persona (default: None).
        """
        if persona_instr is not None:
            self.persona_instr = persona_instr
        else:
            assert (
                persona in Persona
            ), f"persona must be one of {', '.join(Persona)}"
            self.persona_instr = c.persona_instrs[persona]
        self.model = model.value
        self.api_key = api_key
        self.default_enhancer = None

    def enhance(self, text: str) -> str:
        """Return text enhanced by Groq API."""
        return enhancer_gemini(
            self.model, self.persona_instr, self.api_key, text
        )


class GroqEnhancer(BaseEnhancer):
    """
    Enhances text using a Groq API
    (https://console.groq.com/docs/overview).
    """

    def __init__(
        self,
        api_key: str,
        model: GroqModel = GroqModel.LLAMA_3_1_8B_INSTANT,
        persona: Persona = Persona.DEFAULT,
        persona_instr: Optional[str] = None,
    ):
        """
        Parameters
        ----------
        api_key : str
            Your Groq api key.
        groq_model : GroqModel, optional
            the model to use for enhancement, must be one of 'GroqModel'
            enum's attributes (default: GroqModel.LLAMA_3_8B_8192).
        persona : Persona, optional
            The persona to be used for enhancement (default: Persona.DEFAULT).
        persona_instr : Optional[str]
            Custom persona instruction, can be used to give the LLM a custom
            persona (default: None).
        """
        if persona_instr is not None:
            self.persona_instr = persona_instr
        else:
            assert (
                persona in Persona
            ), f"persona must be one of {', '.join(Persona)}"
            self.persona_instr = c.persona_instrs[persona]
        self.model = model
        self.api_key = api_key
        self.default_enhancer = None

    def enhance(self, text: str) -> str:
        """Returns text enhanced by Groq API."""
        return enhancer_groq(
            self.model.value, self.api_key, self.persona_instr, text
        )
