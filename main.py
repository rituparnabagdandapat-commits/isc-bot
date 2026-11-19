# main.py - IndSnpnrKnfrClan Bot
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} 🔥")
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
