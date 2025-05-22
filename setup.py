#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

# Read the contents of README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="openai-toolchain",
    version="0.1.0",
    author="Pneumac",
    author_email="dev@pneumac.com",
    description="A Python library for building and managing OpenAI function tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/openai-toolchain",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"openai_toolchain": ["py.typed"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
            "types-pyyaml>=6.0.0",
            "setuptools>=42.0.0",
            "wheel>=0.37.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/openai-toolchain/issues",
        "Source": "https://github.com/yourusername/openai-toolchain",
    },
)
