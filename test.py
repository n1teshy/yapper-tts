# flake8: noqa: E501

import os
import sys

from yapper import (
    GeminiEnhancer,
    GeminiModel,
    GroqEnhancer,
    GroqModel,
    PiperSpeaker,
)
from yapper.constants import piper_enum_to_lang_code

meta_speaker = PiperSpeaker()
lang_code_to_text = {
    "ar_JO": "\u0642\u064e\u0648\u0652\u0633\u064f \u0642\u064f\u0632\u064e\u062d\u0652\u060c \u064a\u064f\u0633\u064e\u0645\u0651\u064e\u0649 \u0643\u064e\u0630\u064e\u0644\u0650\u0643\u064e: \u0642\u064e\u0648\u0652\u0633\u064f \u0627\u0644\u0652\u0645\u064e\u0637\u064e\u0631\u0650 \u0623\u064e\u0648\u0652 \u0642\u064e\u0648\u0652\u0633\u064f \u0627\u0644\u0652\u0623\u064e\u0644\u0652\u0648\u064e\u0627\u0646\u0650\u060c \u0648\u064e\u0647\u064f\u0648\u064e \u0638\u064e\u0627\u0647\u0650\u0631\u064e\u0629\u064c \u0637\u064e\u0628\u0650\u064a\u0639\u0650\u064a\u0651\u064e\u0629\u064c \u0641\u0650\u0632\u0652\u064a\u064e\u0627\u0626\u0650\u064a\u0651\u064e\u0629\u064c \u0646\u064e\u0627\u062a\u0650\u062c\u064e\u0629\u064c \u0639\u064e\u0646\u0650 \u0627\u0646\u0652\u0643\u0650\u0633\u064e\u0627\u0631\u0650 \u0648\u064e\u062a\u064e\u062d\u064e\u0644\u0651\u064f\u0644\u0650 \u0636\u064e\u0648\u0652\u0621\u0650 \u0627\u0644\u0634\u0651\u064e\u0645\u0652\u0633\u0650 \u062e\u0650\u0644\u0627\u0644\u064e \u0642\u064e\u0637\u0652\u0631\u064e\u0629\u0650 \u0645\u064e\u0627\u0621\u0650 \u0627\u0644\u0652\u0645\u064e\u0637\u064e\u0631\u0650.",
    "ca_ES": "L'arc de Sant Mart\u00ed o arc del cel \u00e9s un fenomen meteorol\u00f2gic \u00f2ptic produ\u00eft per la reflexi\u00f3, refracci\u00f3 i dispersi\u00f3 de la llum causada per gotes d'aigua en suspensi\u00f3 a la troposfera que resulta en l'aparici\u00f3 al cel de l'espectre de la llum visible, interpretat per l'ull hum\u00e0 com els colors vermell, taronja, groc, verd, blau, indi i violat.",
    "cs_CZ": "Duha je fotometeor, projevuj\u00edc\u00ed se jako skupina soust\u0159edn\u00fdch barevn\u00fdch oblouk\u016f, kter\u00e9 vznikaj\u00ed lomem a vnit\u0159n\u00edm odrazem slune\u010dn\u00edho nebo m\u011bs\u00ed\u010dn\u00edho sv\u011btla na vodn\u00edch kapk\u00e1ch v atmosf\u00e9\u0159e.",
    "cy_GB": "Rhyfeddod neu ffenomenon optegol a meteorolegol yw enfys, pan fydd sbectrwm o olau yn ymddangos yn yr awyr pan fo'r haul yn disgleirio ar ddiferion o leithder yn atmosffer y ddaear.",
    "da_DK": 'En regnbue er et optisk f\u00e6nomen; en "lyseffekt", som skabes p\u00e5 himlen, n\u00e5r lys fra Solen rammer sm\u00e5 vanddr\u00e5ber i luften, f.eks. faldende regn.',
    "de_DE": "Der Regenbogen ist ein atmosph\u00e4risch-optisches Ph\u00e4nomen, das als kreisbogenf\u00f6rmiges farbiges Lichtband in einer von der Sonne beschienenen Regenwand oder -wolke wahrgenommen wird.",
    "el_GR": "\u039f\u03b9 \u03b5\u03c0\u03b9\u03c3\u03c4\u03ae\u03bc\u03bf\u03bd\u03b5\u03c2 \u03bc\u03b5\u03bb\u03b5\u03c4\u03bf\u03cd\u03bd \u03b1\u03ba\u03cc\u03bc\u03b7 \u03c4\u03bf \u03bf\u03c5\u03c1\u03ac\u03bd\u03b9\u03bf \u03c4\u03cc\u03be\u03bf.",
    "es_ES": "Un arco\u00edris o arco iris es un fen\u00f3meno \u00f3ptico y meteorol\u00f3gico que consiste en la aparici\u00f3n en el cielo de un arco de luz multicolor, originado por la descomposici\u00f3n de la luz solar en el espectro visible, la cual se produce por refracci\u00f3n, cuando los rayos del sol atraviesan peque\u00f1as gotas de agua contenidas en la atm\u00f3sfera terrestre.",
    "es_MX": "Un arco\u00edris o arco iris es un fen\u00f3meno \u00f3ptico y meteorol\u00f3gico que consiste en la aparici\u00f3n en el cielo de un arco de luz multicolor, originado por la descomposici\u00f3n de la luz solar en el espectro visible, la cual se produce por refracci\u00f3n, cuando los rayos del sol atraviesan peque\u00f1as gotas de agua contenidas en la atm\u00f3sfera terrestre.",
    "fa_IR": "\u0631\u0646\u06af\u06cc\u0646\u200c\u06a9\u0645\u0627\u0646 \u067e\u062f\u06cc\u062f\u0647\u200c\u0627\u06cc \u0646\u0648\u0631\u06cc \u0648 \u06a9\u0645\u0627\u0646\u06cc \u0627\u0633\u062a \u06a9\u0647 \u0632\u0645\u0627\u0646\u06cc \u06a9\u0647 \u062e\u0648\u0631\u0634\u06cc\u062f \u0628\u0647 \u0642\u0637\u0631\u0627\u062a \u0646\u0645 \u0648 \u0631\u0637\u0648\u0628\u062a \u062c\u0648 \u0632\u0645\u06cc\u0646 \u0645\u06cc\u200c\u062a\u0627\u0628\u062f \u0628\u0627\u0639\u062b \u0627\u06cc\u062c\u0627\u062f \u0637\u06cc\u0641\u06cc \u0627\u0632 \u0646\u0648\u0631 \u062f\u0631 \u0622\u0633\u0645\u0627\u0646 \u0645\u06cc\u200c\u0634\u0648\u062f. \u0627\u06cc\u0646 \u067e\u062f\u06cc\u062f\u0647 \u0628\u0647 \u0634\u06a9\u0644 \u06cc\u06a9 \u06a9\u0645\u0627\u0646",
    "fi_FI": "Sateenkaari on spektrin v\u00e4reiss\u00e4 esiintyv\u00e4 ilmakeh\u00e4n optinen ilmi\u00f6.",
    "fr_FR": "Un arc-en-ciel est un photom\u00e9t\u00e9ore, un ph\u00e9nom\u00e8ne optique se produisant dans le ciel, visible dans la direction oppos\u00e9e au Soleil quand il brille pendant la pluie.",
    "hu_HU": "A sziv\u00e1rv\u00e1ny olyan optikai jelens\u00e9g, melyet es\u0151- vagy p\u00e1racseppek okoznak, mikor a f\u00e9ny prizmaszer\u0171en megt\u00f6rik rajtuk \u00e9s sz\u00edneire bomlik, kialakul a sz\u00ednk\u00e9pe, m\u00e1s n\u00e9ven spektruma.",
    "is_IS": "Regnbogi (einnig kalla\u00f0ur fri\u00f0arbogi) er lj\u00f3sfr\u00e6\u00f0ilegt og ve\u00f0urfr\u00e6\u00f0ilegt fyrirb\u00e6ri sem orsakast \u00feegar litr\u00f3f birtist \u00e1 himninum \u00e1 me\u00f0an s\u00f3lin sk\u00edn \u00e1 v\u00e6tu \u00ed andr\u00famslofti jar\u00f0ar.",
    "it_IT": "In fisica dell'atmosfera e meteorologia l'arcobaleno \u00e8 un fenomeno ottico atmosferico che produce uno spettro quasi continuo di luce nel cielo quando la luce del Sole attraversa le gocce d'acqua rimaste in sospensione dopo un temporale, o presso una cascata o una fontana.",
    "ka_GE": "\u10ea\u10d8\u10e1\u10d0\u10e0\u10e2\u10e7\u10d4\u10da\u10d0 \u2014 \u10d0\u10e2\u10db\u10dd\u10e1\u10e4\u10d4\u10e0\u10e3\u10da\u10d8 \u10dd\u10de\u10e2\u10d8\u10d9\u10e3\u10e0\u10d8 \u10d3\u10d0 \u10db\u10d4\u10e2\u10d4\u10dd\u10e0\u10dd\u10da\u10dd\u10d2\u10d8\u10e3\u10e0\u10d8 \u10db\u10dd\u10d5\u10da\u10d4\u10dc\u10d0, \u10e0\u10dd\u10db\u10d4\u10da\u10d8\u10ea \u10ee\u10e8\u10d8\u10e0\u10d0\u10d3 \u10ec\u10d5\u10d8\u10db\u10d8\u10e1 \u10e8\u10d4\u10db\u10d3\u10d4\u10d2 \u10e9\u10dc\u10d3\u10d4\u10d1\u10d0.",
    "kk_KZ": "\u041a\u0435\u043c\u043f\u0456\u0440\u049b\u043e\u0441\u0430\u049b \u2013 \u0430\u0441\u043f\u0430\u043d \u043a\u04af\u043c\u0431\u0435\u0437\u0456\u043d\u0434\u0435 \u0442\u04af\u0440\u043b\u0456 \u0442\u04af\u0441\u0442\u0456 \u0434\u043e\u0493\u0430 \u0442\u04af\u0440\u0456\u043d\u0434\u0435 \u043a\u04e9\u0440\u0456\u043d\u0435\u0442\u0456\u043d \u0430\u0442\u043c\u043e\u0441\u0444\u0435\u0440\u0430\u0434\u0430\u0493\u044b \u043e\u043f\u0442\u0438\u043a\u0430\u043b\u044b\u049b \u049b\u04b1\u0431\u044b\u043b\u044b\u0441.",
    "lb_LU": "Et freet mech, Iech kennen ze l\u00e9ieren.",
    "lv_LV": "Varav\u012bksne ir optiska par\u0101d\u012bba atmosf\u0113r\u0101, kuru rada Saules staru lau\u0161ana un atstaro\u0161ana kr\u012bto\u0161os lietus pilienos.",
    "ne_NP": "\u0907\u0928\u094d\u0926\u094d\u0930\u0947\u0923\u0940 \u0935\u093e \u0907\u0928\u094d\u0926\u094d\u0930\u0927\u0928\u0941\u0937 \u092a\u094d\u0930\u0915\u093e\u0936 \u0930 \u0930\u0902\u0917\u092c\u093e\u091f \u0909\u0924\u094d\u092a\u0928\u094d\u0928 \u092d\u090f\u0915\u094b \u092f\u0938\u094d\u0924\u094b \u0918\u091f\u0928\u093e \u0939\u094b \u091c\u0938\u092e\u093e \u0930\u0902\u0917\u0940\u0928 \u092a\u094d\u0930\u0915\u093e\u0936\u0915\u094b \u090f\u0909\u091f\u093e \u0905\u0930\u094d\u0927\u0935\u0943\u0924 \u0906\u0915\u093e\u0936\u092e\u093e \u0926\u0947\u0916\u093f\u0928\u094d\u091b\u0964 \u091c\u092c \u0938\u0942\u0930\u094d\u092f\u0915\u094b \u092a\u094d\u0930\u0915\u093e\u0936 \u092a\u0943\u0925\u094d\u0935\u0940\u0915\u094b \u0935\u093e\u092f\u0941\u092e\u0923\u094d\u0921\u0932\u092e\u093e \u092d\u090f\u0915\u094b \u092a\u093e\u0928\u0940\u0915\u094b \u0925\u094b\u092a\u093e \u092e\u093e\u0925\u093f \u092a\u0930\u094d\u091b, \u092a\u093e\u0928\u0940\u0915\u094b \u0925\u094b\u092a\u093e\u0932\u0947 \u092a\u094d\u0930\u0915\u093e\u0936\u0932\u093e\u0908 \u092a\u0930\u093e\u0935\u0930\u094d\u0924\u0928, \u0906\u0935\u0930\u094d\u0924\u0928 \u0930 \u0921\u093f\u0938\u094d\u092a\u0930\u094d\u0938\u0928 \u0917\u0930\u094d\u0926\u091b\u0964 \u092b\u0932\u0938\u094d\u0935\u0930\u0941\u092a \u0906\u0915\u093e\u0936\u092e\u093e \u090f\u0909\u091f\u093e \u0938\u092a\u094d\u0924\u0930\u0919\u094d\u0917\u0940 \u0905\u0930\u094d\u0927\u0935\u0943\u0924\u093e\u0915\u093e\u0930 \u092a\u094d\u0930\u0915\u093e\u0936\u0940\u092f \u0906\u0915\u0943\u0924\u093f \u0909\u0924\u094d\u092a\u0928\u094d\u0928 \u0939\u0941\u0928\u094d\u091b\u0964 \u092f\u094b \u0906\u0915\u0943\u0924\u093f\u0932\u093e\u0908 \u0928\u0948 \u0907\u0928\u094d\u0926\u094d\u0930\u0947\u0923\u0940 \u092d\u0928\u093f\u0928\u094d\u091b\u0964 \u0907\u0928\u094d\u0926\u094d\u0930\u0947\u0923\u0940 \u0926\u0947\u0916\u093f\u0928\u0941\u0915\u094b \u0915\u093e\u0930\u0923 \u0935\u093e\u092f\u0941\u092e\u0923\u094d\u0921\u0932\u092e\u093e \u092a\u093e\u0928\u0940\u0915\u093e \u0915\u0923\u0939\u0930\u0941 \u0939\u0941\u0928\u0941 \u0928\u0948 \u0939\u094b\u0964 \u0935\u0930\u094d\u0937\u093e, \u091d\u0930\u0928\u093e\u092c\u093e\u091f \u0909\u091b\u093f\u091f\u094d\u091f\u093f\u090f\u0915\u094b \u092a\u093e\u0928\u0940, \u0936\u0940\u0924, \u0915\u0941\u0939\u093f\u0930\u094b \u0906\u0926\u093f\u0915\u094b \u0907\u0928\u094d\u0926\u094d\u0930\u0947\u0923\u0940 \u0926\u0947\u0916\u093f\u0928\u0947 \u092a\u094d\u0930\u0915\u094d\u0930\u093f\u092f\u093e\u092e\u093e \u092e\u0939\u0924\u094d\u0924\u094d\u0935\u092a\u0942\u0930\u094d\u0923 \u092d\u0942\u092e\u093f\u0915\u093e \u0939\u0941\u0928\u094d\u091b\u0964 \u0907\u0928\u094d\u0926\u094d\u0930\u0947\u0923\u0940\u092e\u093e \u0938\u093e\u0924 \u0930\u0902\u0917\u0939\u0930\u0941 \u0930\u093e\u0924\u094b, \u0938\u0941\u0928\u094d\u0924\u0932\u093e, \u092a\u0939\u0947\u0902\u0932\u094b, \u0939\u0930\u093f\u092f\u094b, \u0906\u0915\u093e\u0936\u0947 \u0928\u093f\u0932\u094b, \u0917\u093e\u0922\u093e \u0928\u093f\u0932\u094b \u0930 \u092c\u0948\u091c\u0928\u0940 \u0930\u0902\u0917 \u0915\u094d\u0930\u092e\u0948\u0938\u0901\u0917 \u0926\u0947\u0916\u093f\u0928\u094d\u091b\u0964 \u092f\u0938\u092e\u093e \u0938\u092c\u0948\u092d\u0928\u094d\u0926\u093e \u092e\u093e\u0925\u093f\u0932\u094d\u0932\u094b \u091b\u0947\u0909\u092e\u093e \u0930\u093e\u0924\u094b \u0930\u0902\u0917 \u0930 \u0905\u0930\u094d\u0915\u094b \u091b\u0947\u0909\u092e\u093e \u092c\u0948\u091c\u0928\u0940 \u0930\u0902\u0917 \u0926\u0947\u0916\u093f\u0928\u094d\u091b\u0964 \u0907\u0928\u094d\u0926\u094d\u0930\u0947\u0923\u0940 \u092a\u0942\u0930\u094d\u0923 \u0935\u0943\u0924\u094d\u0924\u093e\u0915\u093e\u0930 \u0938\u092e\u0947\u0924 \u0939\u0941\u0928 \u0938\u0915\u094d\u0928\u0947 \u092d\u090f \u092a\u0928\u093f \u0938\u093e\u0927\u0930\u0923 \u0905\u0935\u0932\u094b\u0915\u0928\u0915\u0930\u094d\u0924\u093e\u0932\u0947 \u091c\u092e\u093f\u0928 \u092e\u093e\u0925\u093f \u092c\u0928\u0947\u0915\u094b \u0906\u0927\u093e \u092d\u093e\u0917 \u092e\u093e\u0924\u094d\u0930 \u0926\u0947\u0916\u094d\u0928 \u0938\u0915\u093f\u0928\u094d\u091b \u0964",
    "nl_BE": "Een regenboog is een gekleurde cirkelboog die aan de hemel waargenomen kan worden als de, laagstaande, zon tegen een nevel van waterdruppeltjes aan schijnt en de zon zich achter de waarnemer bevindt.",
    "nl_NL": "Een regenboog is een gekleurde cirkelboog die aan de hemel waargenomen kan worden als de, laagstaande, zon tegen een nevel van waterdruppeltjes aan schijnt en de zon zich achter de waarnemer bevindt.",
    "no_NO": "Regnbuen eller regnbogen er et optisk fenomen som oppst\u00e5r n\u00e5r solen skinner gjennom regndr\u00e5per i atmosf\u00e6ren og betrakteren st\u00e5r med solen i ryggen.",
    "pl_PL": "T\u0119cza, zjawisko optyczne i meteorologiczne, wyst\u0119puj\u0105ce w postaci charakterystycznego wielobarwnego \u0142uku powstaj\u0105cego w wyniku rozszczepienia \u015bwiat\u0142a widzialnego, zwykle promieniowania s\u0142onecznego, za\u0142amuj\u0105cego si\u0119 i odbijaj\u0105cego wewn\u0105trz licznych kropli wody maj\u0105cych kszta\u0142t zbli\u017cony do kulistego.",
    "pt_BR": "Um arco-\u00edris, tamb\u00e9m popularmente denominado arco-da-velha, \u00e9 um fen\u00f4meno \u00f3ptico e meteorol\u00f3gico que separa a luz do sol em seu espectro cont\u00ednuo quando o sol brilha sobre got\u00edculas de \u00e1gua suspensas no ar.",
    "pt_PT": "Um arco-íris, também popularmente denominado arco-da-velha, é um fenômeno óptico e meteorológico que separa a luz do sol em seu espectro contínuo quando o sol brilha sobre gotículas de água suspensas no ar.",
    "ro_RO": "Curcubeul este un fenomen optic \u0219i meteorologic atmosferic care se manifest\u0103 prin apari\u021bia pe cer a unui spectru de forma unui arc colorat atunci c\u00e2nd lumina soarelui se refract\u0103 \u00een pic\u0103turile de ap\u0103 din atmosfer\u0103.",
    "ru_RU": "\u0420\u0430\u0434\u0443\u0433\u0430, \u0430\u0442\u043c\u043e\u0441\u0444\u0435\u0440\u043d\u043e\u0435, \u043e\u043f\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0438 \u043c\u0435\u0442\u0435\u043e\u0440\u043e\u043b\u043e\u0433\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u044f\u0432\u043b\u0435\u043d\u0438\u0435, \u043d\u0430\u0431\u043b\u044e\u0434\u0430\u0435\u043c\u043e\u0435 \u043f\u0440\u0438 \u043e\u0441\u0432\u0435\u0449\u0435\u043d\u0438\u0438 \u044f\u0440\u043a\u0438\u043c \u0438\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u043e\u043c \u0441\u0432\u0435\u0442\u0430 \u043c\u043d\u043e\u0436\u0435\u0441\u0442\u0432\u0430 \u0432\u043e\u0434\u044f\u043d\u044b\u0445 \u043a\u0430\u043f\u0435\u043b\u044c.",
    "sk_SK": "D\u00faha je optick\u00fd \u00fakaz vznikaj\u00faci v atmosf\u00e9re Zeme.",
    "sl_SI": "Mavrica je svetlobni pojav v ozra\u010dju, ki ga vidimo v obliki loka spektralnih barv.",
    "sr_RS": "\u0414\u0443\u0433\u0430 \u0458\u0435 \u043e\u043f\u0442\u0438\u0447\u043a\u0430 \u0438 \u043c\u0435\u0442\u0435\u043e\u0440\u043e\u043b\u043e\u0448\u043a\u0430 \u043f\u043e\u0458\u0430\u0432\u0430 \u043a\u043e\u0458\u0438 \u0441\u0435 \u043f\u043e\u0458\u0430\u0432\u0459\u0443\u0458\u0435 \u043d\u0430 \u043d\u0435\u0431\u0443, \u043a\u0430\u0434\u0430 \u0441\u0435 \u0441\u0443\u043d\u0447\u0435\u0432\u0438 \u0437\u0440\u0430\u0446\u0438 \u043f\u0440\u0435\u043b\u0430\u043c\u0430\u0458\u0443 \u043a\u0440\u043e\u0437 \u0441\u0438\u0442\u043d\u0435 \u0432\u043e\u0434\u0435\u043d\u0435 \u043a\u0430\u043f\u0438, \u043d\u0430\u0458\u0447\u0435\u0448\u045b\u0435 \u043d\u0430\u043a\u043e\u043d \u043a\u0438\u0448\u0435.",
    "sv_SE": "En regnb\u00e5ge \u00e4r ett optiskt, meteorologiskt fenomen som upptr\u00e4der som ett fullst\u00e4ndigt ljusspektrum i form av en b\u00e5ge p\u00e5 himlen d\u00e5 solen lyser p\u00e5 nedfallande regn.",
    "sw_CD": "Upinde wa mvua ni tao la rangi mbalimbali angani ambalo linaweza kuonekana wakati Jua huangaza kupitia matone ya mvua inayoanguka.",
    "tr_TR": "G\u00f6kku\u015fa\u011f\u0131, g\u00fcne\u015f \u0131\u015f\u0131nlar\u0131n\u0131n ya\u011fmur damlalar\u0131nda veya sis bulutlar\u0131nda yans\u0131mas\u0131 ve k\u0131r\u0131lmas\u0131yla meydana gelen ve \u0131\u015f\u0131k tayf\u0131 renklerinin bir yay \u015feklinde g\u00f6r\u00fcnd\u00fc\u011f\u00fc meteorolojik bir olayd\u0131r.",
    "uk_UA": "\u0412\u0435\u0441\u0435\u0301\u043b\u043a\u0430, \u0442\u0430\u043a\u043e\u0436 \u0440\u0430\u0301\u0439\u0434\u0443\u0433\u0430 \u043e\u043f\u0442\u0438\u0447\u043d\u0435 \u044f\u0432\u0438\u0449\u0435 \u0432 \u0430\u0442\u043c\u043e\u0441\u0444\u0435\u0440\u0456, \u0449\u043e \u044f\u0432\u043b\u044f\u0454 \u0441\u043e\u0431\u043e\u044e \u043e\u0434\u043d\u0443, \u0434\u0432\u0456 \u0447\u0438 \u0434\u0435\u043a\u0456\u043b\u044c\u043a\u0430 \u0440\u0456\u0437\u043d\u043e\u043a\u043e\u043b\u044c\u043e\u0440\u043e\u0432\u0438\u0445 \u0434\u0443\u0433 ,\u0430\u0431\u043e \u043a\u0456\u043b, \u044f\u043a\u0449\u043e \u0434\u0438\u0432\u0438\u0442\u0438\u0441\u044f \u0437 \u043f\u043e\u0432\u0456\u0442\u0440\u044f, \u0449\u043e \u0441\u043f\u043e\u0441\u0442\u0435\u0440\u0456\u0433\u0430\u044e\u0442\u044c\u0441\u044f \u043d\u0430 \u0442\u043b\u0456 \u0445\u043c\u0430\u0440\u0438, \u044f\u043a\u0449\u043e \u0432\u043e\u043d\u0430 \u0440\u043e\u0437\u0442\u0430\u0448\u043e\u0432\u0430\u043d\u0430 \u043f\u0440\u043e\u0442\u0438 \u0421\u043e\u043d\u0446\u044f.",
    "vi_VN": "C\u1ea7u v\u1ed3ng hay m\u1ed1ng c\u0169ng nh\u01b0 quang ph\u1ed5 l\u00e0 hi\u1ec7n t\u01b0\u1ee3ng t\u00e1n s\u1eafc c\u1ee7a c\u00e1c \u00e1nh s\u00e1ng t\u1eeb M\u1eb7t Tr\u1eddi khi kh\u00fac x\u1ea1 v\u00e0 ph\u1ea3n x\u1ea1 qua c\u00e1c gi\u1ecdt n\u01b0\u1edbc m\u01b0a.",
    "zh_CN": "\u5f69\u8679\uff0c\u53c8\u7a31\u5929\u5f13\u3001\u5929\u8679\u3001\u7d73\u7b49\uff0c\u7c21\u7a31\u8679\uff0c\u662f\u6c23\u8c61\u4e2d\u7684\u4e00\u7a2e\u5149\u5b78\u73fe\u8c61\uff0c\u7576\u592a\u967d \u5149\u7167\u5c04\u5230\u534a\u7a7a\u4e2d\u7684\u6c34\u6ef4\uff0c\u5149\u7dda\u88ab\u6298\u5c04\u53ca\u53cd\u5c04\uff0c\u5728\u5929\u7a7a\u4e0a\u5f62\u6210\u62f1\u5f62\u7684\u4e03\u5f69\u5149\u8b5c\uff0c\u7531\u5916 \u5708\u81f3\u5185\u5708\u5448\u7d05\u3001\u6a59\u3001\u9ec3\u3001\u7da0\u3001\u84dd\u3001\u975b\u84dd\u3001\u5807\u7d2b\u4e03\u79cd\u989c\u8272\uff08\u9713\u8679\u5247\u76f8\u53cd\uff09\u3002",
    "en_US": "A rainbow is a meteorological phenomenon that is caused by reflection, refraction and dispersion of light in water droplets resulting in a spectrum of light appearing in the sky.",
    "en_GB": "A rainbow is a meteorological phenomenon that is caused by reflection, refraction and dispersion of light in water droplets resulting in a spectrum of light appearing in the sky.",
}

lang_code_to_locality = {
    "ar_JO": "Arabic",
    "ca_ES": "Catalan",
    "cs_CZ": "Czech",
    "cy_GB": "Welsh",
    "da_DK": "Danish",
    "de_DE": "German",
    "el_GR": "Greek",
    "es_ES": "Spanish",
    "es_MX": "Spanish",
    "fa_IR": "Persian",
    "fi_FI": "Finnish",
    "fr_FR": "French",
    "hu_HU": "Hungarian",
    "is_IS": "Icelandic",
    "it_IT": "Italian",
    "ka_GE": "Georgian",
    "kk_KZ": "Kazakh",
    "lb_LU": "Luxembourgish",
    "lv_LV": "Latvian",
    "ne_NP": "Nepali",
    "nl_BE": "Dutch",
    "nl_NL": "Dutch",
    "no_NO": "Norwegian",
    "pl_PL": "Polish",
    "pt_BR": "Portuguese",
    "pt_PT": "Portuguese",
    "ro_RO": "Romanian",
    "ru_RU": "Russian",
    "sk_SK": "Slovak",
    "sl_SI": "Slovenian",
    "sr_RS": "Serbian",
    "sv_SE": "Swedish",
    "sw_CD": "Swahili",
    "tr_TR": "Turkish",
    "uk_UA": "Ukrainian",
    "vi_VN": "Vietnamese",
    "zh_CN": "Chinese",
    "en_US": "English",
    "en_GB": "English",
}


def test_enhancers():
    import json
    import random
    import time

    from dotenv import load_dotenv

    load_dotenv()

    groq_key = os.environ["groq_key"]
    gemini_key = os.environ["gemini_key"]
    invalid_models = {str(GroqModel): [], str(GeminiModel): []}

    for model_provider in [GeminiModel, GroqModel]:
        for model in model_provider:
            try:
                print("%r -> %s" % (model_provider.__name__, model.value))
                if model_provider is GroqModel:
                    enhancer = GroqEnhancer(model=model, api_key=groq_key)
                else:
                    enhancer = GeminiEnhancer(model=model, api_key=gemini_key)
                print(enhancer.enhance("hello"))
                time.sleep(random.randint(5, 10))
            except Exception as e:
                invalid_models[str(model_provider)].append(model.value)
                print("error: %r" % (e,))
            finally:
                print("--------")

    if any([len(models) > 0 for models in invalid_models.values()]):
        print(json.dumps(invalid_models))
        return False

    return True


def test_speakers():
    for voice_enum, lang_code in piper_enum_to_lang_code.items():
        for voice in voice_enum:
            locality = lang_code_to_locality[lang_code]
            text = lang_code_to_text[lang_code]
            print("%s -> %s" % (locality, voice.value))
            meta_speaker.say(f"testing {locality} voice.")
            try:
                PiperSpeaker(voice=voice).say(text)
            except Exception as e:
                print("error: %r" % (e,))
                return False
            finally:
                print("--------")
    return True


if __name__ == "__main__":
    test_name = len(sys.argv) > 1 and sys.argv[1]

    if test_name == "enhancers":
        passed = test_enhancers()
    elif test_name == "speakers":
        passed = test_speakers()
    else:
        print("Usage: python test.py [speakers, enhancers]")
        sys.exit(1)

    if not passed:
        print("\033[91m❌ test failed!\033[0m")
        sys.exit(1)
    else:
        print("\033[92m✅ test passed!\033[0m")
