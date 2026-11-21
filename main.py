import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} | ID: {bot.user.id}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

async def main():
    async with bot:
        # Load ALL your files
        await bot.load_extension("tickets")
        await bot.load_extension("chatbot")
        await bot.load_extension("commands")
        await bot.load_extension("welcomemessage")
        print("Loaded: tickets, chatbot, commands, welcomemessage ✅")
        await bot.start(TOKEN)

asyncio.run(main())
