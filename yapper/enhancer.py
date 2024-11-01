from abc import ABC, abstractmethod
from typing import Optional
from urllib.error import URLError

import google.generativeai as genai
from g4f.client import Client
from g4f.errors import RetryProviderError
from google.api_core.exceptions import ResourceExhausted

import yapper.constants as c
from yapper.enums import Gemini, Persona


def enhancer_gpt(
    client: Client, model: str, persona_instr: str, query: str
) -> Optional[str]:
    try:
        messages = [
            {c.FLD_ROLE: c.ROLE_SYSTEM, c.FLD_CONTENT: persona_instr},
            {c.FLD_ROLE: c.ROLE_USER, c.FLD_CONTENT: f'\n\n"{query}"'},
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content
    except (RetryProviderError, URLError):
        return None


def enhancer_gemini(
    client: genai.GenerativeModel, query: str
) -> Optional[str]:
    try:
        return client.generate_content(f'\n\n"{query}"').text
    except ResourceExhausted:
        return None


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
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(
            gemini_model.value,
            system_instruction=self.persona_instr,
        )
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
        enhanced = enhancer_gemini(self.client, text)
        if enhanced is None and self.fallback_to_gpt:
            if self.default_enhancer is None:
                self.default_enhancer = DefaultEnhancer(
                    persona_instr=self.persona_instr, gpt_model=self.gpt_model
                )
            enhanced = self.default_enhancer.enhance(text)
        return enhanced or text
