
# Mega Uploader Bot for Telegram (Koyeb-ready)

This is a background worker Telegram bot that extracts video links from a MEGA.nz folder
and sends them one-by-one to @urluploaderbot, waiting for each to be processed before continuing.

## Features
- Accepts a public MEGA folder link
- Filters only video files (.mp4, .mkv, .avi)
- Sends them one-by-one to @urluploaderbot
- Waits for a media response before sending the next

## Usage
Deploy this on [Koyeb](https://www.koyeb.com) as a **Worker** using this repo and Buildpack type `Python`.
It auto-starts using the included `Procfile`.

## Requirements
- `python-telegram-bot==20.7`
- `mega.py`

## Deploy
Use this repo on Koyeb under the Worker option and link your Telegram Bot Token in `main.py`.
