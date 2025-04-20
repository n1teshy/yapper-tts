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
    GEMMA_2_9B_IT = "gemma2-9b-it"
    LLAMA_3_3_70B_VERSATILE = "llama-3.3-70b-versatile"
    LLAMA_3_1_8B_INSTANT = "llama-3.1-8b-instant"
    LLAMA_GUARD_3_8B = "llama-guard-3-8b"
    LLAMA_2_70B_8192 = "llama3-70b-8192"
    LLAMA_2_8B_8192 = "llama3-8b-8192"
    ALLAM_2_7B = "allam-2-7b"
    DEEPSEEK_R1_DISTILL_LLAMA_70B = "deepseek-r1-distill-llama-70b"
    LLAMA_4_MAVERICK_17B_128E_INSTRUCT = (
        "meta-llama/llama-4-maverick-17b-128e-instruct"
    )
    LLAMA_4_SCOUT_17B_16E_INSTRUCT = (
        "meta-llama/llama-4-scout-17b-16e-instruct"
    )
    QWEN_QWQ_32B = "qwen-qwq-32b"


class GeminiModel(str, Enum):
    GEMINI_2_5_FLASH_PREVIEW_04_17 = "gemini-2.5-flash-preview-04-17"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_1_5_FLASH_8B = "gemini-1.5-flash-8b"
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_2_0_FLASH_THINKING_EXP_01_21 = "gemini-2.0-flash-thinking-exp-01-21"
    GEMINI_2_0_PRO_EXP_02_05 = "gemini-2.0-pro-exp-02-05"
    GEMINI_2_0_FLASH_EXP = "gemini-2.0-flash-exp"
    GEMINI_EXP_1206 = "gemini-exp-1206"
    GEMINI_2_0_FLASH_THINKING_EXP_1219 = "gemini-2.0-flash-thinking-exp-1219"
    GEMINI_1_5_FLASH_8B_EXP_0924 = "gemini-1.5-flash-8b-exp-0924"
    GEMINI_1_5_FLASH_8B_EXP_0827 = "gemini-1.5-flash-8b-exp-0827"
