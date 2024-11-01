from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent.resolve()
meta = {}
exec((ROOT / "yapper/meta.py").read_text(), meta)
NAME, VERSION, GITHUB = meta["name"], meta["version"], meta["github"]
long_description = (ROOT / "README.md").read_text()


setup(
    name=NAME,
    version=VERSION,
    author="Nitesh Yadav",
    author_email="nitesh.txt@gmail.com",
    description="AI powered text-ehancer and offline text-to-speech",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=GITHUB,
    packages=find_packages(),
    install_requires=[
        "google-generativeai==0.8.3",
        "pyttsx3",
        "g4f",
        "pygame",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    platforms="Posix; Windows",
    keywords=[
        "text-to-speech",
        "offline text-to-speech",
        "tts",
        "speech synthesis",
    ],
    python_requires=">=3.9",
    license="MIT",
)
