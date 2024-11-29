import discord
from discord.ext import commands
import aiohttp
from geopy.geocoders import Nominatim
from geopy.point import Point
import datetime
import pytz

class ISSTrackerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.iss_api_url = "http://api.open-notify.org/iss-now.json"
        self.geolocator = Nominatim(user_agent="space_discord_bot")

    async def get_iss_location(self):
        """Fetch current ISS location"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.iss_api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('iss_position', {})
                return None

    def get_nearest_location(self, lat: float, lon: float) -> str:
        """Get the nearest notable location to the coordinates"""
        try:
            point = Point(lat, lon)
            location = self.geolocator.reverse(point, zoom=4, language='en')
            
            if location:
                address = location.raw.get('address', {})
                # Try to get the most relevant location name
                for key in ['city', 'state', 'country']:
                    if place := address.get(key):
                        return place
                return location.address.split(',')[0]
            
            # If no land location found, determine ocean
            if lon > -180 and lon < 180:
                if lat > 0:
                    return "North "
                else:
                    return "South "
                
                if lon > 0:
                    return "Eastern Ocean"
                else:
                    return "Western Ocean"
            
            return "Unknown Location"
        except Exception:
            return "Location Unavailable"

    @commands.command(name='iss')
    async def iss_location(self, ctx):
        """Get the current location of the International Space Station"""
        async with ctx.typing():
            if position := await self.get_iss_location():
                lat = float(position.get('latitude', 0))
                lon = float(position.get('longitude', 0))
                
                location = self.get_nearest_location(lat, lon)
                current_time = datetime.datetime.now(pytz.UTC)

                embed = discord.Embed(
                    title="🛸 ISS Current Location",
                    description="Real-time tracking of the International Space Station",
                    color=discord.Color.blue(),
                    timestamp=current_time
                )

                embed.add_field(
                    name="Coordinates",
                    value=f"🌍 Latitude: {lat:.2f}°\n🌎 Longitude: {lon:.2f}°",
                    inline=False
                )

                embed.add_field(
                    name="Nearest Location",
                    value=f"📍 {location}",
                    inline=False
                )

                # Add NASA's ISS live stream
                embed.add_field(
                    name="Live Stream",
                    value="[Watch ISS Live](https://www.nasa.gov/nasalive)",
                    inline=False
                )

                # Add map link
                map_url = f"https://www.google.com/maps/@{lat},{lon},4z"
                embed.add_field(
                    name="View on Map",
                    value=f"[Open in Google Maps]({map_url})",
                    inline=False
                )

                embed.set_footer(text="Data provided by Open Notify API")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Unable to fetch ISS location. Please try again later.")

async def setup(bot):
    await bot.add_cog(ISSTrackerCog(bot))
