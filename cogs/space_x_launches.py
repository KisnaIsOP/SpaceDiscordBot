import discord
from discord.ext import commands, tasks
import aiohttp
import datetime
import pytz
from typing import Optional, Dict, Any

class SpaceXLaunchesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spacex_api_url = "https://api.spacexdata.com/v4"
        self.launch_check.start()
        self.cached_next_launch: Optional[Dict[str, Any]] = None
        self.last_check = datetime.datetime.now(pytz.UTC)

    def cog_unload(self):
        self.launch_check.cancel()

    @tasks.loop(minutes=30)
    async def launch_check(self):
        """Check for upcoming launches every 30 minutes"""
        await self.fetch_next_launch()

    async def fetch_next_launch(self):
        """Fetch the next launch data from SpaceX API"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.spacex_api_url}/launches/next") as response:
                if response.status == 200:
                    self.cached_next_launch = await response.json()
                    self.last_check = datetime.datetime.now(pytz.UTC)

    def format_launch_embed(self, launch_data: Dict[str, Any]) -> discord.Embed:
        """Format launch data into a Discord embed"""
        embed = discord.Embed(
            title=f"🚀 Next SpaceX Launch: {launch_data.get('name', 'Unknown Mission')}",
            color=discord.Color.blue()
        )

        # Launch time
        launch_time = datetime.datetime.fromisoformat(
            launch_data.get('date_utc', '').replace('Z', '+00:00')
        )
        embed.add_field(
            name="Launch Time",
            value=f"<t:{int(launch_time.timestamp())}:F>",
            inline=False
        )

        # Details
        details = launch_data.get('details', 'No details available.')
        embed.add_field(name="Mission Details", value=details[:1024], inline=False)

        # Links
        links = launch_data.get('links', {})
        if webcast := links.get('webcast'):
            embed.add_field(name="Livestream", value=f"[Watch Here]({webcast})", inline=True)
        
        if patch := links.get('patch', {}).get('small'):
            embed.set_thumbnail(url=patch)

        embed.set_footer(text=f"Last updated: {self.last_check.strftime('%Y-%m-%d %H:%M UTC')}")
        return embed

    @commands.command(name='launch')
    async def next_launch(self, ctx):
        """Get information about the next SpaceX launch"""
        if not self.cached_next_launch:
            await self.fetch_next_launch()
        
        if self.cached_next_launch:
            embed = self.format_launch_embed(self.cached_next_launch)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Unable to fetch launch data. Please try again later.")

    @launch_check.before_loop
    async def before_launch_check(self):
        """Wait for the bot to be ready before starting the launch check loop"""
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(SpaceXLaunchesCog(bot))
