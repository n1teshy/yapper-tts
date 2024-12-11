from enum import Enum


class Persona(str, Enum):
    DEFAULT = "companion"
    JARVIS = "jarvis"
    FRIDAY = "friday"
    ALFRED = "alfred"
    HAL = "HAL"
    CORTANA = "cortana"
    SAMANTHA = "samantha"
    TARS = "TARS"


class GeminiModel(str, Enum):
    PRO_1_5_LATEST = "gemini-1.5-pro-latest"
    PRO_1_5_002 = "gemini-1.5-pro-002"
    PRO_1_5_EXP_0801 = "gemini-1.5-pro-exp-0801"
    PRO_1_5_EXP_0827 = "gemini-1.5-pro-exp-0827"
    FLASH_1_5_1_5_LATEST = "gemini-1.5-flash-latest"
    FLASH_1_5_1_5_001 = "gemini-1.5-flash-001"
    FLASH_1_5_001_TUNING = "gemini-1.5-flash-001-tuning"
    FLASH_1_5 = "gemini-1.5-flash"
    FLASH_1_5_EXP_0827 = "gemini-1.5-flash-exp-0827"
    FLASH_1_5_002 = "gemini-1.5-flash-002"
    FLASH_1_5_8B = "gemini-1.5-flash-8b"
    FLASH_1_5_8B_001 = "gemini-1.5-flash-8b-001"
    FLASH_1_5_8B_LATEST = "gemini-1.5-flash-8b-latest"
    FLASH_1_5_8B_EXP_0827 = "gemini-1.5-flash-8b-exp-0827"
    FLASH_1_5_8B_EXP_0924 = "gemini-1.5-flash-8b-exp-0924"


class PiperVoiceUS(str, Enum):
    AMY = "amy"
    ARCTIC = "arctic"
    BRYCE = "bryce"
    JOHN = "john"
    NORMAN = "norman"
    DANNY = "danny"
    HFC_FEMALE = "hfc_female"
    HFC_MALE = "hfc_male"
    JOE = "joe"
    KATHLEEN = "kathleen"
    KRISTIN = "kristin"
    LJSPEECH = "ljspeech"
    KUSAL = "kusal"
    L2ARCTIC = "l2arctic"
    LESSAC = "lessac"
    LIBRITTS = "libritts"
    LIBRITTS_R = "libritts_r"
    RYAN = "ryan"


class PiperVoiceUK(str, Enum):
    ALAN = "alan"
    ALBA = "alba"
    ARU = "aru"
    CORI = "cori"
    JENNY_DIOCO = "jenny_dioco"
    NORTHERN_ENGLISH_MALE = "northern_english_male"
    SEMAINE = "semaine"
    SOUTHERN_ENGLISH_FEMALE = "southern_english_female"
    VCTK = "vctk"


class PiperQuality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class GroqModel(str, Enum):
    LLAMA_3_8B_8192 = "llama3-8b-8192"
    LLAMA_3_GROQ_70B_8192_TOOL_USE_PREVIEW = (
        "llama3-groq-70b-8192-tool-use-preview"
    )
    LLAMA_3_GROQ_8B_8192_TOOL_USE_PREVIEW = (
        "llama3-groq-8b-8192-tool-use-preview"
    )
    LLAMA_3_70B_8192 = "llama3-70b-8192"
    LLAMA_3_1_8B_INSTANT = "llama-3.1-8b-instant"
    LLAMA_3_2_1B_PREVIEW = "llama-3.2-1b-preview"
    LLAMA_3_2_3B_PREVIEW = "llama-3.2-3b-preview"
    LLAMA_3_2_11B_VISION_PREVIEW = "llama-3.2-11b-vision-preview"
    LLAMA_3_2_90B_VISION_PREVIEW = "llama-3.2-90b-vision-preview"
    LLAMA_3_3_70B_VERSATILE = "llama-3.3-70b-versatile"
    LLAMA_3_3_70B_SPECDEC = "llama-3.3-70b-specdec"
    LLAMA_GUARD_3_8B = "llama-guard-3-8b"
    GEMMA_2_9B_IT = "gemma2-9b-it"
    GEMMA_7B_IT = "gemma-7b-it"
    MIXTRAL_8X7B_32768 = "mixtral-8x7b-32768"
