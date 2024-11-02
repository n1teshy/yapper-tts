import threading
from functools import wraps
from types import TracebackType
from typing import Callable, Optional

import yapper.meta as meta
from yapper.enhancer import BaseEnhancer, DefaultEnhancer
from yapper.speaker import BaseSpeaker, DefaultSpeaker


class Yapper:
    def __init__(
        self,
        enhancer: Optional[BaseEnhancer] = None,
        speaker: Optional[BaseSpeaker] = None,
        plain: bool = False,
        block: bool = True,
        use_stdout: bool = False,
    ):
        """
        Parameters
        ----------
        enhancer : Optional[BaseEnhancer]
            enhancer to be used for enhancing text
            (default: DefaultEnhancer).
        speaker : Optional[BaseSpeaker]
            speaker to be used for speaking the text
            (default: DefaultSpeaker).
        plain : bool, optional
            Do not enhance text, say it as it is (default: False).
        block: bool, optional
            wait for speech-syntheis to complete (default: True).
        use_stdout: bool, optional
            print the enhanced text before saying it (default: False).
        """
        self.enhancer = enhancer or DefaultEnhancer()
        self.speaker = speaker or DefaultSpeaker()
        self.plain = plain
        self.block = block
        self.use_stdout = use_stdout

    def yap(
        self,
        text: str,
        plain: Optional[bool] = None,
        block: Optional[bool] = None,
        use_stdout: Optional[bool] = None,
    ):
        """
        Speaks the given text.

        Parameters
        ----------
        text : str
            The text to speak.
        plain : bool, optional
            Do not enhance text, say it as it is.
        block: Optional[bool]
            wait for speech-syntheis to complete.
        use_stdout: bool, optional
            print the enhanced text before saying it.
        """
        if plain is None:
            plain = self.plain
        if block is None:
            block = self.block
        if use_stdout is None:
            use_stdout = self.use_stdout

        def func(
            text: str,
            plain: bool,
            use_stdout: bool,
        ):
            if not plain:
                text = self.enhancer.enhance(text)
            if use_stdout:
                print(f"{meta.name}: {text}")
            self.speaker.say(text)

        if block:
            func(text, plain, use_stdout)
        else:
            threading.Thread(
                target=func, args=(text, plain, use_stdout)
            ).start()

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[Exception],
        exc_value: Optional[str],
        tb: Optional[TracebackType],
    ):
        if exc_type:
            err = exc_type.__name__ + (f"\n{exc_value}" if exc_value else "")
            self.yap(err)
        return not exc_type

    def __call__(self, on_call: bool = False, pass_yapper: bool = False):
        """
        Parameters
        ----------
        on_call : bool, optional
            announce when the decorated function starts running
            (default: False).
        pass_yapper: bool, optional
            pass the yapper instance to the decorated function as a
            keyword argument 'yapper' when it is called (default: False).
        """

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if on_call:
                    f_desc = f"running function {func.__name__}"
                    if func.__doc__ is not None:
                        f_desc += "\n" + f"description: {func.__doc__}"
                    self.yap(f_desc)
                try:
                    if not pass_yapper:
                        return func(*args, **kwargs)
                    return func(*args, **kwargs, yapper=self.yap)
                except Exception as e:
                    err = e.__class__.__name__
                    desc = str(e)
                    if desc:
                        err = f"{err}: {desc}"
                    self.yap(err)
                    raise e

            return wrapper

        return decorator
