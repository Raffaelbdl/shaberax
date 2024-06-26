# Shaberax: A multipurpose logging library

![Python Version](https://img.shields.io/badge/Python->=3.10-blue)
![Code Style](https://img.shields.io/badge/Code_Style-black-black)

[**Installation**](#installation) | [**Overview**](#overview) 

## Installation
This package requires Python 3.10 or later.
You can install all functionalities using the following commands:

```bash
pip install --upgrade pip
pip install "shaberax[all] @ git+https://github.com/Raffaelbdl/shaberax.git"
```

For single-functionality installations, please refer to the [**Overview**](#overview) section.

## Overview 
### General Logger
The General Logger is an all-purpose logger. 

Example Usage:
```python
from shaberax.logger import GeneralLogger

GeneralLogger.warning("Warning message")
GeneralLogger.start_debug()
GeneralLogger.debug("Debug message")
```

### Telegram
You can install the telegram logger using the following commands:
```bash
pip install --upgrade pip
pip install "shaberax[telegram] @ git+https://github.com/Raffaelbdl/shaberax.git"
```

> [!IMPORTANT]
> To use the telegram logger, please follow the instructions at the top of:
https://github.com/Raffaelbdl/shaberax/blob/master/shaberax/telegram.py

Example Usage:
```python
from shaberax.telegram import TelegramLogger

TelegramLogger.setup(TOKEN, CHAT_ID)
TelegramLogger.log_text("Text to send")
```
