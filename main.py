# main.py - IndSnpnrKnfrClan Bot
import discord
from discord.ext import commands
import os

# --- FILES ADD ---
import GROQ           # GROQ.py - BIG LETTER
import chatbot        # chatbot.py - small
import commands       # commands.py - small
import WelcomeMessage # WelcomeMessage.py

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} 🔥")
    print(f"Bot Name: {os.getenv('BOT_NAME')}")
    await bot.load_extension("chatbot")
    await bot.load_extension("commands")
    await bot.load_extension("WelcomeMessage")
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} cmds ✅")
    print("IndSnpnrKnfrClan is ONLINE!")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(os.getenv("TOKEN"))
