# GANimebot
Telegram bot that converts images using [UGATIT](https://github.com/taki0112/UGATIT) framework

## Requirements
  - aiogram==2.13
  - numpy==1.16.4
  - opencv-python==4.5.2.54
  - Pillow==8.2.0
  - tensorflow==1.14.0

## Installation
  - git clone https://github.com/RadianceX/ganimebot --recurse-submodules
  - virtualenv venv
  - source ./venv/Scripts/activate
  - pip install -r requirements.txt
  - set your API_TOKEN in ./bot.conf file

## Start the bot
  - python ganimebot.py

## Checkpoints for UGATIT model
  - [selfie2anime checkpoint (50 epoch)](https://drive.google.com/file/d/1V6GbSItG3HZKv3quYs7AP0rr1kOCT3QO/view?usp=sharing)
  - [selfie2anime checkpoint (100 epoch)](https://drive.google.com/file/d/19xQK2onIy-3S5W5K-XIh85pAg_RNvBVf/view?usp=sharing)
