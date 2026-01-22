# Schedujoe

A plain HTML project that tracks the games [Joseph Anderson](https://www.twitch.tv/andersonjph/) has, is, or will stream.

Deploys using Github Pages to https://schedujoe.bulder.fi

## schedujoe-generator

This project also contains a simple static site generator written in Python.
The `generator.py` script takes in the `generator_data.yaml` file, and generates an updated `index.html` file.

Prerequisites:
* Python 3.12 or higher
* beautifulsoup4 (Used for pretty printing the HTML)