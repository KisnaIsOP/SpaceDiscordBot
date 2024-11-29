# Space Discord Bot

A feature-rich Discord bot that provides space facts, NASA's Astronomy Picture of the Day, and space trivia games.

## Features

- `!spacefact` - Get random space facts
- `!dailyupdate` - View NASA's Astronomy Picture of the Day
- `!trivia` - Play space trivia games
- `!help` - View all available commands

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with:
   ```
   DISCORD_TOKEN=your_token_here
   NASA_API_KEY=your_nasa_api_key_here
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## Hosting

This bot can be hosted on:
- Railway.app (Recommended)
- Heroku
- DigitalOcean

## Environment Variables

- `DISCORD_TOKEN`: Your Discord bot token
- `NASA_API_KEY`: Your NASA API key
