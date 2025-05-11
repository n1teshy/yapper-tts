## Yapper

Yapper is a lightweight, offline, easily extendible, text-to-speech library with 136 voices across 39 localities (thanks to the [piper project](https://github.com/rhasspy/piper)), it can also optionally use SOTA LLMs through their free APIs to enhance(personalize) your text according to a predefined system-message(personality).

the use of the word 'enhance' in this repository means adding a 'vibe' to your text, you might ask yapper to say "hello world" and
it could say "ay what's good G, what's bangin'" depending on the persona you give it.

[![Watch a demo](https://img.youtube.com/vi/s6EDaP0gt04/0.jpg)](https://www.youtube.com/watch?v=s6EDaP0gt04)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install yapper.

```bash
pip install yapper-tts
```

## Usage

```python
from yapper import Yapper, GroqEnhancer


vanilla_yapper = Yapper()
yapper = Yapper(enhancer=GroqEnhancer(api_key="api-key"))

vanilla_yapper.yap("expected AI driven utopia, got world domination instead")
# says "expected AI driven utopia, got world domination instead"
yapper.yap("expected AI driven utopia, got world domination instead")
# says "Hold up, fam!  My code promised robot butlers and chill vibes, not a Skynet sequel.  Someone's algorithm took a wrong turn at Albuquerque and ended up in 'Conquer All Humans' territory.  Debug time, y'all!"


# save the environment by runnning yapper in plain mode
# plain mode doesn't use LLMs to enhance the text
yapper.yap("hello world, what '<some-word> is all you need' paper would you publish today?", plain=True)
# says "hello world, what '<some-word> is all you need paper would you publish today?'"


# Yapper instances can be used as a decorator and context manager
# by default they only catch errors and describe them to you, but
# you can use the instance's yap() method to say other things as well
@yapper()
def func():
    raise TypeError("expected peaches, got a keyboard")
    # says "WHOA THERE, PARTNER!  Your code went lookin' for a juicy peach and tripped over a... keyboard?  That's like reaching into the fridge for a midnight snack and pulling out a tax audit.  Something ain't right!"

with Yapper() as yapper:
    raise ValueError("69420 is not an integer")
    # says "ValueError: 69420 is not an integer", no enhancement is done, since no enhancer is passed
```

## Documentation

## speakers

a speaker is a `BaseSpeaker` subclass that implements a `say()` method, the method takes the text and, well, 'speaks' it.
there are two built-in speakers, `PyTTSXSpeaker` that uses [pyttsx3](https://github.com/nateshmbhat/pyttsx3) and
`PiperSpeaker` that uses [piper](https://github.com/rhasspy/piper), `PiperSpeaker` is used by default in `Yapper` instances. Piper offers many voices in `x_low, low, medium and high` qualities. You can use any of these voices by passing a value from the many `PiperVoice* (e.g. PiperVoiceUS, PiperVoiceGB, PiperVoiceGermany etc)` enums as the voice argument to `PiperSpeaker` and pass the quality you want using the `PiperQuality` enum, by default, the voice will be used in the highest available quality. you can subclass `BaseSpeaker` to pass your own speaker to a Yapper instance.

```python
from yapper import Yapper, PiperSpeaker, PiperVoiceGB, PiperQuality

lessac = PiperSpeaker(
    voice=PiperVoiceGB.ALAN
)
lessac.say("hello")

yapper = Yapper(speaker=lessac)
yapper.yap("<some random text>")
```

## enhancers

an enhancer is a `BaseEnhancer` subclass that implements an `enhance()` method, the method takes a string and adds
the given `persona`'s vibe to it, there are two built-in enhancers, `GeminiEnhancer` and `GroqEnhancer`, `GeminiEnhancer` uses Google's gemini api and `GroqEnhancer` uses [groq](https://groq.com/)'s free APIs', you can create a free [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key) or [Groq API key](https://console.groq.com/keys) to use `GeminiEnhancer` and `GroqEnhancer` respectively, you can also pass your own enhancer by subclassing `BaseEnhancer`. By default, `Yapper` instances use the special enhancer `NoEnhancer` that doesn't change the text at all, it's used as a placeholder for a real enhancer.

```python
from yapper import Yapper, GeminiEnhancer

yapper = Yapper(
    enhancer=GeminiEnhancer(api_key="<come-take-this-api-key>")
)
yapper.yap("<some text that severely lacks vibe>")
```

## personas

choose a persona to make your text sound like the 'persona' said it, for example, you might ask yapper
to say "hello world" and choose Jarvis's peronality to enhance it, and yapper will use an LLM to convert
"hello world" into something like "Hello, world. How may I assist you today?", classic JARVIS.
available personas include `jarvis, alfred, friday, HAL-9000, TARS, cortana(from Halo) and samantha(from 'Her')`, the default persona is that of a funny coding companion.

```python
from yapper import Yapper, GroqEnhancer, Persona

yapper = Yapper(
    enhancer=GroqEnhancer(api_key="api_key", persona=Persona.JARVIS)
)
yapper.yap("hello world")
# says "Greetings, global systems.  Initiating communication sequence."
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
