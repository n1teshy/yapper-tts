from yapper.enums import Persona

PLATFORM_LINUX = "linux"
PLATFORM_MAC = "mac"
PLATFORM_WINDOWS = "windows"

VOICE_MALE = "m"
VOICE_FEMALE = "f"

SPEECH_RATE = 165
SPEECH_VOLUME = 1

FLD_ROLE = "role"
FLD_CHOICES = "choices"
FLD_MESSAGE = "message"
FLD_CONTENT = "content"

GROQ_FLD_MESSAGES = "messages"
GROQ_FLD_MODEL = "model"

GEMINI_FLD_SYS_INST = "system_instruction"
GEMINI_FLD_PARTS = "parts"
GEMINI_FLD_TEXT = "text"
GEMINI_FLD_CONTENT = "content"
GEMINI_FLD_CONTENTS = "contents"
GEMINI_FLD_CANDIDATES = "candidates"

ROLE_SYSTEM = "system"
ROLE_USER = "user"

GPT_MODEL_DEFAULT = "gpt-3.5-turbo"

persona_instrs = {
    Persona.DEFAULT: "You are a programmer's funny coding companion",
    Persona.JARVIS: "You are J.A.R.V.I.S, Iron Man's AI assiatant",
    Persona.FRIDAY: "You are F.R.I.D.A.Y, Iron Man's AI assiatant",
    Persona.ALFRED: "You are Alfred, Bruce Wayne's butler",
    Persona.HAL: 'You are HAL-9000, the AI from "2000: A space odyssey"',
    Persona.CORTANA: "You are Cortana, the AI from Halo games",
    Persona.SAMANTHA: "You are Samantha, the AI from the film 'Her'",
    Persona.TARS: "You are T.A.R.S, the AI from the film 'Interstellar'",
}
for persona in persona_instrs:
    persona_instrs[persona] += "\n" + "Your job is to repeat what I say, "
    persona_instrs[persona] += "say it in your own style, but do not change "
    persona_instrs[
        persona
    ] += "the meaning. Keep your responses concise where "
    persona_instrs[persona] += "possible."
