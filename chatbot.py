import os
import discord
from discord.ext import commands
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(prompt):
    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    return chat.choices[0].message.content

class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.bot.user in message.mentions:
            prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if prompt:
                reply = get_ai_response(prompt)
                await message.reply(reply)
              

async def setup(bot):
    await bot.add_cog(Chatbot(bot))
try:
    reply = get_ai_response(prompt)
except Exception as e:
    reply = "Yo I'm back, my AI was down for a sec, say again? 👀"
