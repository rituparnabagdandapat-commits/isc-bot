import os, discord
from discord.ext import commands
from groq import Groq

client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(prompt):
    try:
        res = client_groq.chat.completions.create(
            model="llama-3.1-8b-instant", # OLD 3.3 model was DELETED by Groq
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return res.choices[0].message.content
    except:
        return "Yo I'm back, my AI was down for a sec, say again? 👀"

class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.bot.user in message.mentions:
            prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip() or "yo"
            reply = get_ai_response(prompt)
            await message.reply(reply)

async def setup(bot):
    await bot.add_cog(Chatbot(bot))
