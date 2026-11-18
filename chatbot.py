# chatbot.py - Sirf CHAT ke liye, NO slash command
import discord
from discord.ext import commands
from groq import get_ai_response

class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # 1. Bot khud ka message ignore kare
        if message.author.bot:
            return

        # 2. Sirf tab reply kare jab:
        # - Bot ko mention kiya ho OR
        # - #ai-chat / #chatbot wale channel me ho OR
        # - DM me ho
        is_mentioned = self.bot.user in message.mentions
        is_dm = isinstance(message.channel, discord.DMChannel)
        is_ai_channel = message.channel.name in ["ai-chat", "chatbot", "chat", "general", "isc-chat"]

        if not (is_mentioned or is_dm or is_ai_channel):
            return

        # 3. Agar mention kiya hai to mention hata de
        clean_msg = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
        if not clean_msg:
            clean_msg = "hi"

        # 4. Typing dikhaye - lagge bot soch raha hai
        async with message.channel.typing():
            reply = await get_ai_response(clean_msg)

        # 5. Reply kare
        await message.reply(reply)

async def setup(bot):
    await bot.add_cog(Chatbot(bot))
