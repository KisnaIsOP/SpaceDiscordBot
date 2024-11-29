import discord
import asyncio
import random
from discord.ext import commands

class SpaceTriviaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trivia_questions = [
            {
                "question": "What is the largest planet in our solar system?",
                "answer": "Jupiter",
                "options": ["Saturn", "Jupiter", "Neptune", "Uranus"]
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "answer": "Mars",
                "options": ["Venus", "Mercury", "Mars", "Jupiter"]
            },
            {
                "question": "What is the name of Earth's natural satellite?",
                "answer": "Moon",
                "options": ["Moon", "Titan", "Europa", "Phobos"]
            },
            {
                "question": "Which is the hottest planet in our solar system?",
                "answer": "Venus",
                "options": ["Mercury", "Venus", "Mars", "Jupiter"]
            },
            {
                "question": "What is the name of the galaxy containing our solar system?",
                "answer": "Milky Way",
                "options": ["Andromeda", "Milky Way", "Triangulum", "Sombrero"]
            }
        ]
        self.active_games = set()

    @commands.command(name='trivia')
    async def trivia(self, ctx):
        """Start a space trivia game"""
        if ctx.channel.id in self.active_games:
            await ctx.send("A trivia game is already active in this channel!")
            return

        self.active_games.add(ctx.channel.id)
        question_data = random.choice(self.trivia_questions)
        
        # Create embed for question
        embed = discord.Embed(
            title="🚀 Space Trivia",
            description=question_data["question"],
            color=discord.Color.blue()
        )
        
        # Add options
        options = question_data["options"]
        random.shuffle(options)
        option_text = "\n".join([f"{idx+1}. {option}" for idx, option in enumerate(options)])
        embed.add_field(name="Options", value=option_text, inline=False)
        embed.set_footer(text="You have 15 seconds to answer! Type the number of your answer.")
        
        await ctx.send(embed=embed)

        def check(m):
            return (m.channel == ctx.channel and 
                   m.content.isdigit() and 
                   1 <= int(m.content) <= len(options))

        try:
            msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            user_answer = options[int(msg.content) - 1]
            
            if user_answer.lower() == question_data["answer"].lower():
                await ctx.send(f"🎉 Correct, {msg.author.mention}! The answer is {question_data['answer']}!")
            else:
                await ctx.send(f"❌ Sorry {msg.author.mention}, that's wrong. The correct answer is {question_data['answer']}!")
                
        except asyncio.TimeoutError:
            await ctx.send(f"⏰ Time's up! The correct answer was {question_data['answer']}!")
        finally:
            self.active_games.remove(ctx.channel.id)
