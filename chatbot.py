import os, discord
from discord.ext import commands
from groq import Groq

TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
client_groq = Groq(api_key=GROQ_KEY)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

def get_ai_response(prompt):
    try:
        res = client_groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return res.choices[0].message.content
    except:
        return "Yo I'm back, my AI was down for a sec, say again? 👀"

@bot.event
async def on_ready():
    print(f"ISC ONLINE as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user in message.mentions:
        prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if not prompt:
            prompt = "yo"
        reply = get_ai_response(prompt)
        await message.reply(reply)
    await bot.process_commands(message)

async def setup_hook():
    await bot.load_extension("commands")

bot.setup_hook = setup_hook

bot.run(TOKEN)
