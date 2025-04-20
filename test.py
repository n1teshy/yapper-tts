import os
import sys

from yapper import (
    GeminiEnhancer,
    GeminiModel,
    GroqEnhancer,
    GroqModel,
    PiperSpeaker,
    PiperVoiceUK,
    PiperVoiceUS
)


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
                print("%r -> %s" % (model_provider, model.value))
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
    for voice_enum in [PiperVoiceUS, PiperVoiceUK]:
        for voice in voice_enum:
            print("%r -> %s" % (voice_enum, voice.value))
            try:
                PiperSpeaker(voice=voice, show_progress=False).say(
                    "Hi, I'm %s" % (voice.value)
                )
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
