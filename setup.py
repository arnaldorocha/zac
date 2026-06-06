"""
Zac Personal Assistant - Package Configuration
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zac-assistant",
    version="1.0.0",
    author="Arnaldo",
    author_email="arnaldorochafilho@gmail.com",
    description="Zac - Personal AI Assistant running locally on Windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arnaldorocha/zac",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Multimedia :: Sound/Speech",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "zac=main:main",
        ],
    },
    include_package_data=True,
    install_requires=[
        "pydantic>=2.5.3",
        "python-dotenv>=1.0.1",
        "vosk>=0.3.45",
        "PyAudio>=0.2.13",
        "pyttsx3>=2.90",
        "playwright>=1.40.0",
        "pygsheets>=2.0.6",
        "openpyxl>=3.10.10",
        "pandas>=2.1.4",
        "fastapi>=0.109.2",
        "uvicorn>=0.27.0",
        "colorlog>=6.8.0",
    ],
)
