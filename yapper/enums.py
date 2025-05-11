from enum import Enum


class PiperVoice(str, Enum):
    pass


class PiperVoiceJordan(PiperVoice):
    KAREEM = "kareem"


class PiperVoiceCatalonia(PiperVoice):
    UPC_ONA = "upc_ona"
    UPC_PAU = "upc_pau"


class PiperVoiceCzech(PiperVoice):
    JIRKA = "jirka"


class PiperVoiceWales(PiperVoice):
    BU_TTS = "bu_tts"
    GWRYW_GOGLEDDOL = "gwryw_gogleddol"


class PiperVoiceDenmark(PiperVoice):
    TALESYNTESE = "talesyntese"


class PiperVoiceGermany(PiperVoice):
    EVA_K = "eva_k"
    KARLSSON = "karlsson"
    KERSTIN = "kerstin"
    MLS = "mls"
    PAVOQUE = "pavoque"
    RAMONA = "ramona"
    THORSTEN = "thorsten"
    THORSTEN_EMOTIONAL = "thorsten_emotional"


class PiperVoiceGreece(PiperVoice):
    RAPUNZELINA = "rapunzelina"


class PiperVoiceSpain(PiperVoice):
    CARLFM = "carlfm"
    DAVEFX = "davefx"
    MLS_10246 = "mls_10246"
    MLS_9972 = "mls_9972"
    SHARVARD = "sharvard"


class PiperVoiceMexico(PiperVoice):
    ALD = "ald"
    CLAUDE = "claude"


class PiperVoiceIran(PiperVoice):
    AMIR = "amir"
    GANJI = "ganji"
    GANJI_ADABI = "ganji_adabi"
    GYRO = "gyro"
    REZA_IBRAHIM = "reza_ibrahim"


class PiperVoiceFinland(PiperVoice):
    HARRI = "harri"


class PiperVoiceFrance(PiperVoice):
    GILLES = "gilles"
    MLS = "mls"
    MLS_1840 = "mls_1840"
    SIWIS = "siwis"
    TOM = "tom"
    UPMC = "upmc"


class PiperVoiceHungary(PiperVoice):
    ANNA = "anna"
    BERTA = "berta"
    IMRE = "imre"


class PiperVoiceIceland(PiperVoice):
    BUI = "bui"
    SALKA = "salka"
    STEINN = "steinn"
    UGLA = "ugla"


class PiperVoiceItaly(PiperVoice):
    PAOLA = "paola"
    RICCARDO = "riccardo"


class PiperVoiceGeorgia(PiperVoice):
    NATIA = "natia"


class PiperVoiceKazakhstan(PiperVoice):
    ISEKE = "iseke"
    ISSAI = "issai"
    RAYA = "raya"


class PiperVoiceLuxembourg(PiperVoice):
    MARYLUX = "marylux"


class PiperVoiceLatvia(PiperVoice):
    AIVARS = "aivars"


class PiperVoiceNepal(PiperVoice):
    GOOGLE = "google"


class PiperVoiceBelgium(PiperVoice):
    NATHALIE = "nathalie"
    RDH = "rdh"


class PiperVoiceNetherlands(PiperVoice):
    MLS = "mls"
    MLS_5809 = "mls_5809"
    MLS_7432 = "mls_7432"
    PIM = "pim"
    RONNIE = "ronnie"


class PiperVoiceNorway(PiperVoice):
    TALESYNTESE = "talesyntese"


class PiperVoicePoland(PiperVoice):
    DARKMAN = "darkman"
    GOSIA = "gosia"
    MC_SPEECH = "mc_speech"


class PiperVoiceBrazil(PiperVoice):
    CADU = "cadu"
    EDRESSON = "edresson"
    FABER = "faber"
    JEFF = "jeff"


class PiperVoicePortugal(PiperVoice):
    TUGAO = "tugão"


class PiperVoiceRomania(PiperVoice):
    MIHAI = "mihai"


class PiperVoiceRussia(PiperVoice):
    DENIS = "denis"
    DMITRI = "dmitri"
    IRINA = "irina"
    RUSLAN = "ruslan"


class PiperVoiceSlovakia(PiperVoice):
    LILI = "lili"


class PiperVoiceSlovenia(PiperVoice):
    ARTUR = "artur"


class PiperVoiceSerbia(PiperVoice):
    SERBSKI_INSTITUT = "serbski_institut"


class PiperVoiceSweden(PiperVoice):
    LISA = "lisa"
    NST = "nst"


class PiperVoiceCongo(PiperVoice):
    LANFRICA = "lanfrica"


class PiperVoiceTurkey(PiperVoice):
    DFKI = "dfki"
    FAHRETTIN = "fahrettin"
    FETTAH = "fettah"


class PiperVoiceUkraine(PiperVoice):
    LADA = "lada"
    UKRAINIAN_TTS = "ukrainian_tts"


class PiperVoiceVietnam(PiperVoice):
    HOURS_SINGLE = "25hours_single"
    VAIS1000 = "vais1000"
    VIVOS = "vivos"


class PiperVoiceChina(PiperVoice):
    HUAYAN = "huayan"


class PiperVoiceUS(PiperVoice):
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
    REZA_IBRAHIM = "reza_ibrahim"
    SAM = "sam"


class PiperVoiceGB(PiperVoice):
    ALAN = "alan"
    ALBA = "alba"
    ARU = "aru"
    CORI = "cori"
    JENNY_DIOCO = "jenny_dioco"
    NORTHERN_ENGLISH_MALE = "northern_english_male"
    SEMAINE = "semaine"
    SOUTHERN_ENGLISH_FEMALE = "southern_english_female"
    VCTK = "vctk"


class PiperVoice(Enum):
    JORDAN = PiperVoiceJordan
    CATALONIA = PiperVoiceCatalonia
    CZECH = PiperVoiceCzech
    WALES = PiperVoiceWales
    DENMARK = PiperVoiceDenmark
    GERMANY = PiperVoiceGermany
    GREECE = PiperVoiceGreece
    SPAIN = PiperVoiceSpain
    MEXICO = PiperVoiceMexico
    IRAN = PiperVoiceIran
    FINLAND = PiperVoiceFinland
    FRANCE = PiperVoiceFrance
    HUNGARY = PiperVoiceHungary
    ICELAND = PiperVoiceIceland
    ITALY = PiperVoiceItaly
    GEORGIA = PiperVoiceGeorgia
    KAZAKHSTAN = PiperVoiceKazakhstan
    LUXEMBOURG = PiperVoiceLuxembourg
    LATVIA = PiperVoiceLatvia
    NEPAL = PiperVoiceNepal
    BELGIUM = PiperVoiceBelgium
    NETHERLANDS = PiperVoiceNetherlands
    NORWAY = PiperVoiceNorway
    POLAND = PiperVoicePoland
    BRAZIL = PiperVoiceBrazil
    PORTUGAL = PiperVoicePortugal
    ROMANIA = PiperVoiceRomania
    RUSSIA = PiperVoiceRussia
    SLOVAKIA = PiperVoiceSlovakia
    SLOVENIA = PiperVoiceSlovenia
    SERBIA = PiperVoiceSerbia
    SWEDEN = PiperVoiceSweden
    CONGO = PiperVoiceCongo
    TURKEY = PiperVoiceTurkey
    UKRAINE = PiperVoiceUkraine
    VIETNAM = PiperVoiceVietnam
    CHINA = PiperVoiceChina
    US = PiperVoiceUS
    GB = PiperVoiceGB


class PiperQuality(str, Enum):
    X_LOW = "x_low"
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


class Persona(str, Enum):
    DEFAULT = "companion"
    JARVIS = "jarvis"
    FRIDAY = "friday"
    ALFRED = "alfred"
    HAL = "HAL"
    CORTANA = "cortana"
    SAMANTHA = "samantha"
    TARS = "TARS"
