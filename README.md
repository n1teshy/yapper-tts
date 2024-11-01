## Yapper

Yapper is a lightweight, offline, real-time, easily extendible, text-to-speech library with more than a dozen voices, it can also, optionally use SOTA LLMs through free APIs to enhance(personalize) your text according to a predefined system-message(personality).

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
from yapper import Yapper


yapper = Yapper()
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

with yapper as yapper:
    raise ValueError("69420 is not an integer")
    # says "Hold up, buddy!  Your code's got a little *existential crisis*. It's lookin' for a whole number, a nice, clean integer.  But it stumbled upon 69420, and it's just... confused.  69420 *might* look like an integer, walks like an integer, but deep down, in the bits and bytes, somethin' ain't right.  Double-check its type, maybe it's wearin' a float disguise.  Or maybe it's just havin' a bad day.  It happens."
```

## Documentation

## speakers
a speaker is a `BaseSpeaker` subclass that implements a `say()` method, the method takes the text and, well, 'speaks' it.
there are two built-in speakers, `DefaultSpeaker` that uses [pyttsx3](https://github.com/nateshmbhat/pyttsx3) and
`PiperSpeaker` that uses [piper](https://github.com/rhasspy/piper), I suggest using `PiperSpeaker` over the default
because of how natural it sounds and it's also 'very' fast, might make piper the default speaker in future, and of course
you can subclass `BaseSpeaker` to pass your own speaker to a Yapper instance. Piper offers many voices in `low, medium and high` qualities, you can use any of them by passing a value from `PiperVoice` enum as the voice argument to `PiperSpeker`.

```python
from yapper import Yapper, PiperSpeaker, PiperVoice, PiperQuality

lessac = PiperSpeaker(
    voice=PiperVoice.LESSAC,
    quality=PiperQuality.HIGH
)
lessac.say("hello")

yapper = Yapper(speaker=lessac)
yapper.yap("<some random text>")
```

## enhancers
an enhancer is `BaseEnhancer` subclass that implements an `enhance()` method, the method takes a string and adds
the given `persona`'s vibe to it, there are two built-in enhancers `DefaultEnhancer` and `GeminiEnhancer`, `DefaultEnhancer`
uses the [g4f](https://github.com/xtekky/gpt4free) to transform text and `GeminiEnhancer` uses Google's gemini api to do the same, you can create a free GCP account and get a gemini api-key for free to use `GeminiEnhancer`, you can pass your own enhancer by subclassing `BaseEnhancer`.

NOTE: `BaseEnhancer` may or may not work, use `GeminiEnhancer` for stability.
NOTE: if an enhancer doesn't work, yapper will say the text as it is.
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
available personas include `jarvis, alfred, friday, HAL-9000, TARS, cortana(from Halo) and samantha(from 'Her')`, the default
persona is that of a funny coding companion.
```python
from yapper import Yapper, DefaultEnhancer, Persona

yapper = Yapper(
    enhancer=DefaultEnhancer(persona=Persona.JARVIS)
)
yapper.yap("hello world")
# says "Greetings, global systems.  Initiating communication sequence."
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
