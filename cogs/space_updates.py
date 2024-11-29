import os
import discord
import requests
from discord.ext import commands
from datetime import datetime

class SpaceUpdatesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nasa_api_key = os.getenv('NASA_API_KEY')
        self.apod_url = "https://api.nasa.gov/planetary/apod"

    @commands.command(name='dailyupdate')
    async def daily_update(self, ctx):
        """Fetches and displays NASA's Astronomy Picture of the Day"""
        if not self.nasa_api_key:
            await ctx.send("Error: NASA API key not found. Please set NASA_API_KEY in .env file")
            return

        try:
            # Fetch APOD data from NASA API
            params = {
                'api_key': self.nasa_api_key,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            response = requests.get(self.apod_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Create embed message
            embed = discord.Embed(
                title=data['title'],
                description=data['explanation'][:2048],  # Discord's limit is 2048 characters
                color=discord.Color.dark_purple(),
                url="https://apod.nasa.gov/apod/astropix.html"
            )
            
            # Add image if available
            if data.get('hdurl'):
                embed.set_image(url=data['hdurl'])
            elif data.get('url'):
                embed.set_image(url=data['url'])

            embed.set_footer(text=f"NASA Astronomy Picture of the Day - {data.get('date', 'Today')}")
            
            await ctx.send(embed=embed)

        except requests.exceptions.RequestException as e:
            await ctx.send(f"Error fetching NASA APOD data: {str(e)}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {str(e)}")
