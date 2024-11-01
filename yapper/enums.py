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


class Gemini(str, Enum):
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


class PiperVoice(str, Enum):
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


class PiperQuality(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
