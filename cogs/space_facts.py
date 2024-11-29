import random
import discord
from discord.ext import commands

class SpaceFactsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.space_facts = [
            "A year on Mercury is just 88 days long.",
            "Venus is the hottest planet in our solar system.",
            "The Sun contains 99.86% of the mass in our solar system.",
            "One day on Venus is longer than one year on Earth.",
            "Jupiter has the shortest day of all the planets.",
            "The Milky Way galaxy will collide with the Andromeda Galaxy in about 5 billion years.",
            "The footprints on the Moon will be there for 100 million years.",
            "Space is completely silent.",
            "The largest known star, UY Scuti, is 1,700 times larger than our Sun.",
            "Light from the Sun takes 8 minutes to reach Earth."
        ]

    @commands.command(name='spacefact')
    async def space_fact(self, ctx):
        """Sends a random space fact"""
        # Create an embed for the space fact
        embed = discord.Embed(
            title="🌟 Random Space Fact",
            description=random.choice(self.space_facts),
            color=discord.Color.dark_blue()
        )
        embed.set_footer(text="Use !spacefact for another fascinating fact!")
        
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Error creating embed. Here's a space fact: " + 
                         random.choice(self.space_facts))
