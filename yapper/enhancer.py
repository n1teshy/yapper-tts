import json
from abc import ABC, abstractmethod
from typing import Optional
from urllib.request import Request, urlopen

from g4f.client import Client

import yapper.constants as c
from yapper.enums import Gemini, Persona


def enhancer_gpt(
    client: Client, model: str, persona_instr: str, query: str
) -> Optional[str]:
    messages = [
        {c.FLD_ROLE: c.ROLE_SYSTEM, c.FLD_CONTENT: persona_instr},
        {c.FLD_ROLE: c.ROLE_USER, c.FLD_CONTENT: query},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content


def enhancer_gemini(
    model: str, sys_inst: str, api_key: str, query: str
) -> str:
    base = "https://generativelanguage.googleapis.com/v1beta/models"
    url = f"{base}/{model}:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        c.GEMINI_FLD_SYS_INST: {
            c.GEMINI_FLD_PARTS: {c.GEMINI_FLD_TEXT: sys_inst}
        },
        c.GEMINI_FLD_CONTENTS: {
            c.GEMINI_FLD_PARTS: {c.GEMINI_FLD_TEXT: query}
        },
    }
    request = Request(
        url, headers=headers, data=json.dumps(data).encode("utf-8")
    )
    with urlopen(request) as response:
        data = json.loads(response.read())
        return data[c.GEMINI_FLD_CANDIDATES][0][c.GEMINI_FLD_CONTENT][
            c.GEMINI_FLD_PARTS
        ][0][c.GEMINI_FLD_TEXT]


class BaseEnhancer(ABC):
    """
    Base class for text enhancers

    Methods
    ----------
    enhance(text: str) -> str
        Enhances the given text.
    """

    @abstractmethod
    def enhance(self, text: str) -> str:
        pass


class DefaultEnhancer(BaseEnhancer):
    def __init__(
        self,
        persona: Persona = Persona.DEFAULT,
        persona_instr: Optional[str] = None,
        gpt_model: str = c.GPT_MODEL_DEFAULT,
    ):
        """
        Enhances text using a GPT model.

        Parameters
        ----------
        persona : str, optional
            The persona to be used for enhancement (default: Persona.DEFAULT).
        persona_instr : Optional[str]
            Instructions specific to the persona (default: None).
        gpt_model : str, optional
            The GPT model to be used for enhancement (default: gpt-3.5-turbo).
        """
        if persona_instr is not None:
            self.persona_instr = persona_instr
        else:
            assert (
                persona in Persona
            ), f"persona must be one of {', '.join(Persona)}"
            self.persona_instr = c.persona_instrs[persona]
        self.model = gpt_model
        self.client = Client()

    def enhance(self, text: str) -> str:
        """
        Enhances the given text.

        Returns
        ----------
        str
            Returns enhanced text, or original text if enhancement fails.
        """
        enhanced = enhancer_gpt(
            self.client, self.model, self.persona_instr, text
        )
        return enhanced or text


class GeminiEnhancer(BaseEnhancer):
    def __init__(
        self,
        api_key: str,
        gemini_model: Gemini = Gemini.PRO_1_5_002,
        persona: Persona = Persona.DEFAULT,
        persona_instr: Optional[str] = None,
        fallback_to_default: bool = False,
        gpt_model: str = c.GPT_MODEL_DEFAULT,
    ):
        """
        Enhances text using a Gemini model.

        Parameters
        ----------
        api_key : str
            Your gemini api key.
        gemini_model : str, optional
            the gemini model to use for enhancement, must be one of 'Gemini'
            enum's attributes. (default: Gemini.PRO_1_5_002)
        persona : str, optional
            The persona to be used for enhancement (default: Persona.DEFAULT).
        persona_instr : Optional[str]
            Instructions specific to the persona (default: None).
        fallback_to_default: bool, optional
            Whether DefaultEnhancer be used in case GeminiEnhancer fails.
            (default: False)
        gpt_model : str, optional
            The GPT model to be used for enhancement if fallback_to_default
            is 'True'. (default: gpt-3.5-turbo).
        """
        if persona_instr is not None:
            self.persona_instr = persona_instr
        else:
            assert (
                persona in Persona
            ), f"persona must be one of {', '.join(Persona)}"
            self.persona_instr = c.persona_instrs[persona]
        self.model = gemini_model
        self.api_key = api_key
        self.default_enhancer = None
        self.fallback_to_gpt = fallback_to_default
        self.gpt_model = gpt_model

    def enhance(self, text: str) -> str:
        """
        Enhances the given text using a Gemini model

        Returns
        ----------
        str
            Returns enhanced text, or original text if enhancement fails.
        """
        try:
            return enhancer_gemini(
                self.model.value, self.persona_instr, self.api_key, text
            )
        except Exception:
            if self.fallback_to_gpt:
                if self.default_enhancer is None:
                    self.default_enhancer = DefaultEnhancer(
                        persona_instr=self.persona_instr,
                        gpt_model=self.gpt_model,
                    )
                return self.default_enhancer.enhance(text)
            else:
                raise
