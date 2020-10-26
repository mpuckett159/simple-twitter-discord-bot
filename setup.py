#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "tweepy>=3.9",
    "discord-webhook",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Marcus Puckett",
    python_requires=">=3.5",
    description="A simple bot for monitoring a Twitter account and sending the messages to Discord.",
    entry_points={
        "console_scripts": ["signal-scanner-bot=simple_twitter_discord_bot.main:main"],
    },
    install_requires=requirements,
    include_package_data=True,
    keywords="signal_scanner_bot",
    name="signal_scanner_bot",
    packages=find_packages(include=["signal_scanner_bot", "signal_scanner_bot.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/mpuckett259/signal-scanner-bot",
    version="0.0.1",
    zip_safe=False,
)
