import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs.space_facts import SpaceFactsCog
from cogs.space_updates import SpaceUpdatesCog
from cogs.space_trivia import SpaceTriviaCog
from cogs.space_x_launches import SpaceXLaunchesCog
from cogs.iss_tracker import ISSTrackerCog

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot configuration
class SpaceBot(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        
    async def setup_hook(self):
        # Load all cogs
        await self.add_cog(SpaceFactsCog(self))
        await self.add_cog(SpaceUpdatesCog(self))
        await self.add_cog(SpaceTriviaCog(self))
        await self.add_cog(SpaceXLaunchesCog(self))
        await self.add_cog(ISSTrackerCog(self))
        
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is active in {len(self.guilds)} guilds.')
        await self.change_presence(activity=discord.Game(name="!help for commands"))

def main():
    # Create bot instance with default prefix '!'
    bot = SpaceBot(command_prefix='!')
    
    # Error handling for missing token
    if not TOKEN:
        raise ValueError("No Discord token found. Please set DISCORD_TOKEN in .env file")
    
    # Run the bot
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
