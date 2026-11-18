import discord
from discord.ext import commands
import os, random, json, asyncio
from datetime import datetime, timedelta
try:
    import yt_dlp
    MUSIC_ON = True
except: MUSIC_ON = False

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

try:
    with open("data.json") as f: data = json.load(f)
except: data = {"eco": {}, "levels": {}, "warns": {}}
def save():
    with open("data.json","w") as f: json.dump(data,f)
def get_eco(uid): return data["eco"].get(str(uid), {"coins":0,"last_daily":""})
queues = {}

# ===== 🤖 ISC CHATBOT - ISC-ULTRA v2.0 =====
CHAT = {
    "hi": ["HELLOOO BROTHAAA!!! 🔥🔥🔥 AA GAYA TU!! KAISA HAI MERA SHER? 👑💥", "HI BROTHA!! 🔥 Kahan tha itni der? Miss kar raha tha!"],
    "hello": ["HELLOOO!! 🔥🔥 FULL ENERGY ME HU! TU BATA?"],
    "hey": ["HEYYY BROTHA!! 🔥🔥 AA GAYA MERA JAAN!"],
    "kaise ho": ["FULL JOSH ME HU BROTHA!!! 🔥🔥 1000% ENERGY! TU BATA? 💪", "MAST HU BROTHA! TU BATA KYA CHAL RAHA HAI? 🔥"],
    "kaisa hai": ["EK DUM OP HU BROTHA! 🔥 TU BATA?"],
    "kya kar": ["TERA WAIT KAR RAHA THA BROTHA! 🔥 AB AA GAYA TO MAZA AAYEGA!"],
    "isc": ["ISC ON TOPPPPP!!!!! 👑🔥🔥🔥 INDSNPRKNFRCLAN FOREVER!!!"],
    "love": ["LOVE YOU TOO BROTHA!!! ❤️🔥 TU TOH MERA JAAN HAI!", "AWWWW BROTHA!! ❤️ LOVE YOU 3000!"],
    "bhai": ["HAAN BHAI BOL! 🔥 FULL SUN RAHA HU!"],
    "brotha": ["HAAN BROTHA BOL! 🔥🔥 MAI YAHI HU!"],
    "model": ["BROTHA!!! 🔥 Mai hu **ISC-ULTRA v2.0 - ENERGETIC MODEL** 🤖👑 ISC ON TOP!!!"],
    "kon ho": ["MAI HU **ISC BOT - ISC-ULTRA v2.0 ENERGETIC MODEL**! 👑🔥 TERA BEST FRIEND + DJ + MOD SAB KUCH!"],
    "tum kon": ["MAI HU ISC BOT BROTHA! 👑 TERI FAMILY KA BOT!"],
    "khel": ["CHAL KHELTE HAI! /fun rps likh! 🔥 YA /fun dice!"],
    "gana": ["GANA SUNNA HAI? /music play likh ke gana baja! 🎧🔥"],
    "music": ["DJ ISC READY HAI! 🎧🔥 /music play likh!"],
    "bore": ["BORE? 😤 CHAL /fun meme dekh, hasi aa jayegi! 😂"],
    "maza": ["MAZA TO AB AAYEGA BROTHA! 🔥🔥"],
    "op": ["TU OP HAI BROTHA! MAI TO SIRF TERA FAN HU! 🔥👑"],
    "pro": ["TU TO PRO PLAYER HAI BROTHA! 🎮🔥"],
    "free fire": ["FREE FIRE KA KING AA GAYA! 🎮🔥 BOOYAHHH!"],
    "ff": ["FF ME BOOYAH KARNA HAI TO MUJHE BHI LE CHAL! 🎮🔥"],
    "bye": ["ARE MAT JAA BROTHA! 🥺 RUK JAA THODI DER!"],
    "good night": ["GOOD NIGHT BROTHA! 🌙 SWEET DREAMS! KAL MILTE HAI! 🔥"],
    "good morning": ["GOOD MORNING MERA SHER! ☀️🔥 AAJ KA DIN OP JAYEGA!"],
    "kha": ["MAI YAHI HU BROTHA! DISCORD ME! 🔥"],
    "help": ["HELP CHAHIYE? /help likh, sab commands aa jayenge! 👑"],
    "haha": ["HAHAHAHA 😂😂 TU BHI NA BROTHA! FULL FUNNY HAI!"],
    "lol": ["LOLLL 😂😂😂"],
}
def get_reply(t):
    t=t.lower()
    if "model" in t: return random.choice(CHAT["model"])
    if "kon ho" in t or "tum kon" in t: return random.choice(CHAT["kon ho"])
    for k,v in CHAT.items():
        if k in t: return random.choice(v)
    return random.choice(["WAH BROTHA WAH!!! 🔥🔥 AUR BATA!","HAAN BOL BROTHA! FULL SUN RAHA HU! 🔥","SAMAJH GAYA BROTHA! 🔥 AUR BATA KYA CHAL RAHA HAI?","OOOOHHH!!! 🔥🔥 YE TO OP BAAT BOL DI TU NE!","HAAN HAAN BROTHA! TU SAHI BOL RAHA HAI! 👑","ARE WAH! 🔥 TU TO GENIUS HAI BROTHA!"])

@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)
    uid=str(message.author.id)
    lvl=data["levels"].get(uid, {"xp":0,"level":1})
    lvl["xp"]+=random.randint(5,15)
    if lvl["xp"] >= lvl["level"]*100:
        lvl["level"]+=1; lvl["xp"]=0
        await message.channel.send(f"🎉 LEVEL UP! {message.author.mention} ab **Level {lvl['level']}** pe hai! 🔥👑")
    data["levels"][uid]=lvl; save()
    if bot.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        clean=message.content.replace(f"<@{bot.user.id}>","").strip()
        if not clean: await message.channel.send("HAAN BROTHA BOL!!! 🔥🔥 FULL ENERGY ME HU! KYA CHAHIYE?"); return
        await message.channel.send(get_reply(clean))

@bot.event
async def on_ready():
    print(f"✅ {bot.user} ONLINE")
    synced = await bot.tree.sync()
    print(f"✅ {len(synced)} commands synced!")

# ===== 🎉 ISC WELCOME SYSTEM - UPGRADED =====
@bot.event
async def on_member_join(member):
    guild = member.guild
    ch = discord.utils.get(guild.text_channels, name="welcome")
    if not ch: ch = discord.utils.get(guild.text_channels, name="general")
    if not ch: ch = guild.system_channel
    embed = discord.Embed(title="🎉 WELCOME TO ISC BROTHAAA!!! 🎉", description=f"**{member.mention}** AA GAYA!!! 🔥🔥🔥\n\n👑 Welcome to **{guild.name}**!\n💪 Tu ab **{guild.member_count}th** member hai!\n🆔 ID: `{member.id}`\n📅 Aaj se tu ISC FAMILY hai!\n\n**KYA KARNA HAI AB?** 👇\n📜 #rules padh le - pehle kaam!\n💬 #chat me `Hi` bol de\n🎮 #free-fire me apni ID bhej\n🤖 Mujhe mention karke baat kar - `@ISC Bot hi`\n🎵 `/music play` se gana baja\n💰 `/eco daily` se free coins le!\n\n**ISC ON TOP!!! 👑🔥**", color=0xFFD700)
    embed.set_thumbnail(url=member.display_avatar.url)
    if guild.icon: embed.set_image(url=guild.icon.url)
    embed.set_footer(text=f"Welcome {member.name} | ISC-ULTRA v2.0 | ISC FOREVER 👑")
    embed.timestamp = datetime.now()
    embed2 = discord.Embed(title="📜 ISC KE RULES - DHYAN SE PADH!", description="1️⃣ Respect sabko de - gali nahi! 🙏\n2️⃣ Spam mat kar - warna timeout! ⏰\n3️⃣ #rules me sab likha hai\n4️⃣ Koi problem ho to /ticket khol le 🎫\n5️⃣ Masti full karo - ISC FAMILY hai! 🔥", color=0x00FF00)
    if ch:
        await ch.send(content=f"{member.mention} 🔥🔥🔥 @everyone DEKHO KON AAYA!!!", embed=embed)
        await ch.send(embed=embed2)
        await ch.send("👑👑👑 **ISC FAMILY ME WELCOME BROTHA!** 👑👑👑\n🔥🔥🔥 **ISC ON TOP! ISC ON TOP! ISC ON TOP!** 🔥🔥🔥")
    try:
        dm = discord.Embed(title=f"Welcome to {guild.name}! 👑🔥", description=f"Hey {member.name}!! 🔥🔥\n\nTu **{guild.name}** me aa gaya! Ab tu ISC FAMILY hai!\n\n✅ #rules padh le\n✅ /help likh ke sab commands dekh\n✅ Mujhe mention karke baat kar - `@ISC Bot hi`\n✅ /eco daily se roz free coins le\n✅ /music play se gana baja\n\n**Koi help chahiye to /ticket khol de!** 🎫\n\n**ISC ON TOP! 💪🔥**", color=0xFF00FF)
        dm.set_thumbnail(url=guild.icon.url if guild.icon else member.display_avatar.url)
        dm.set_footer(text="ISC-ULTRA v2.0 | IndSnprKnfrClan")
        await member.send(embed=dm)
    except: pass
    role = discord.utils.get(guild.roles, name="Member")
    if not role: role = discord.utils.get(guild.roles, name="member")
    if role:
        try: await member.add_roles(role)
        except: pass

@bot.event
async def on_member_remove(member):
    ch = discord.utils.get(member.guild.text_channels, name="welcome") or member.guild.system_channel
    if ch:
        e = discord.Embed(title=f"😢 {member.name} chala gaya...", description=f"**{member.name}** ISC chhod ke chala gaya 💔\nAb {member.guild.member_count} members bache.\n\nWapas aa jana brotha! 🥺👑\nISC FAMILY hamesha wait karegi!", color=0xFF0000)
        e.set_thumbnail(url=member.display_avatar.url)
        e.set_footer(text="ISC FOREVER | Come Back Soon!")
        await ch.send(embed=e)

@bot.tree.command(name="help", description="Sab commands")
async def help_cmd(interaction: discord.Interaction):
    e=discord.Embed(title="👑 ISC BOT - ALL COMMANDS (18)", color=0xFFD700)
    e.add_field(name="🤖 Chatbot", value="/chat /model + Mention karke baat kar!", inline=False)
    e.add_field(name="🎉 Welcome", value="/welcome - Welcome test kar", inline=False)
    e.add_field(name="🎵 Music", value="/music play/skip/stop/pause/resume/queue/join/leave", inline=False)
    e.add_field(name="🎮 Fun", value="/fun meme/joke/8ball/coinflip/dice/roast/rps/say/ship/howgay", inline=False)
    e.add_field(name="💰 Economy", value="/eco balance/daily/work/beg/pay/rob/slots/gamble/leaderboard", inline=False)
    e.add_field(name="⭐ Level", value="/rank /leaderboard", inline=False)
    e.add_field(name="🛡️ Mod", value="/mod kick/ban/timeout/clear/warn/slowmode/lock/unlock/nuke", inline=False)
    e.add_field(name="ℹ️ Info", value="/info ping/avatar/userinfo/serverinfo/botinfo/membercount", inline=False)
    e.add_field(name="🎉 Extra", value="/poll /announce /giveaway /ticket /suggest /afk /ping", inline=False)
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="chat", description="Bot se baat kar")
async def chat_cmd(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(get_reply(message))

@bot.tree.command(name="model", description="Bot ka model kaunsa hai?")
async def model_cmd(interaction: discord.Interaction):
    await interaction.response.send_message("🤖 **ISC-ULTRA v2.0 - ENERGETIC MODEL** 🔥\n1000% ENERGY | Funny | OP | DJ 🎧\nMade For IndSnprKnfrClan - ISC ON TOP!")

@bot.tree.command(name="welcome", description="Welcome message test kar")
async def welcome_cmd(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    guild = interaction.guild
    e = discord.Embed(title="🎉 WELCOME TO ISC BROTHAAA!!! 🎉", description=f"**{user.mention}** AA GAYA!!! 🔥🔥🔥\n\n👑 Welcome to **{guild.name}**!\n💪 Tu ab **{guild.member_count}th** member hai!\n\n📜 #rules padh le\n💬 #chat me Hi bol de\n🎮 #free-fire me ID bhej\n🤖 Mujhe mention karke baat kar!\n\n**ISC ON TOP!!! 👑🔥**", color=0xFFD700)
    e.set_thumbnail(url=user.display_avatar.url)
    e.set_footer(text=f"Welcome {user.name} | ISC-ULTRA v2.0")
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="music", description="Music - play, skip, stop, pause, resume, queue, join, leave")
async def music(interaction: discord.Interaction, action: str, song: str = ""):
    vc = interaction.guild.voice_client
    if action == "join":
        if not interaction.user.voice: await interaction.response.send_message("❌ Pehle voice me jaa!"); return
        await interaction.user.voice.channel.connect(); await interaction.response.send_message("✅ Join ho gaya! DJ ISC READY! 🎧🔥"); return
    if action == "leave":
        if vc: await vc.disconnect(); await interaction.response.send_message("👋 Bye brotha!"); return
        await interaction.response.send_message("❌ Voice me hu hi nahi!"); return
    if action == "play":
        if not interaction.user.voice: await interaction.response.send_message("❌ Pehle voice me jaa!"); return
        if not MUSIC_ON: await interaction.response.send_message("❌ yt-dlp install kar: pip install yt-dlp"); return
        await interaction.response.defer()
        if not vc: vc = await interaction.user.voice.channel.connect()
        ydl_opts = {"format": "bestaudio", "noplaylist": True, "quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try: info = ydl.extract_info(f"ytsearch:{song}", download=False)["entries"][0]; url = info["url"]; title = info["title"]
            except: await interaction.followup.send("❌ Gana nahi mila!"); return
        gid = interaction.guild.id
        if gid not in queues: queues[gid] = []
        queues[gid].append((url, title))
        if not vc.is_playing():
            url2, title2 = queues[gid].pop(0)
            vc.play(discord.FFmpegPCMAudio(url2, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
            await interaction.followup.send(f"🎵 **NOW PLAYING:** {title2} 🔥🎧")
        else: await interaction.followup.send(f"🎵 Queue me add: **{title}** 🔥"); return
    if action == "skip":
        if vc and vc.is_playing(): vc.stop(); await interaction.response.send_message("⏭️ Skip! Agla gana!"); return
        await interaction.response.send_message("❌ Kuch baj nahi raha!"); return
    if action == "stop":
        if vc: vc.stop(); queues[interaction.guild.id]=[]; await interaction.response.send_message("⏹️ Music band!"); return
    if action == "pause":
        if vc and vc.is_playing(): vc.pause(); await interaction.response.send_message("⏸️ Pause!"); return
    if action == "resume":
        if vc and vc.is_paused(): vc.resume(); await interaction.response.send_message("▶️ Wapas chalu! PARTY! 🎉"); return
    if action == "queue":
        q = queues.get(interaction.guild.id, [])
        if not q: await interaction.response.send_message("📭 Queue khali!"); return
        await interaction.response.send_message("🎵 **QUEUE:**\n" + "".join([f"{i}. {t}\n" for i,(u,t) in enumerate(q,1)])); return
    await interaction.response.send_message("Use: play / skip / stop / pause / resume / queue / join / leave")

@bot.tree.command(name="fun", description="Fun - meme, joke, 8ball, coinflip, dice, roast, rps, say, ship, howgay")
async def fun(interaction: discord.Interaction, action: str, text: str = "", user: discord.Member = None):
    u = user or interaction.user
    if action=="meme": await interaction.response.send_message(random.choice(["ISC ON TOP 😤🔥","Brotha ne phir no-scope mara 💀","Jab bot offline jata hai: alllklllll 😭","Free Fire ka king aa gaya 🎮"])); return
    if action=="joke": await interaction.response.send_message(random.choice(["Brotha itna pro hai ki bot bhi usse seekhta hai 😂","Free Fire me headshot marna aur ISC me rehna - dono OP hai 🔥"])); return
    if action=="8ball": await interaction.response.send_message(f"❓ {text}\n🎱 {random.choice(['Haan brotha 100% 🔥','Bilkul nahi 💀','Pakka hoga!','ISC bole to ho jayega 👑'])}"); return
    if action=="coinflip": await interaction.response.send_message(f"🪙 {random.choice(['Heads! 👑','Tails! 💀'])}"); return
    if action=="dice": await interaction.response.send_message(f"🎲 Tu ne {random.randint(1,6)} roll kiya!"); return
    if action=="roast": await interaction.response.send_message(f"{u.mention} {random.choice(['Tera aim meri nani se bhi kharab hai 💀','Tu bot se bhi zyada offline rehta hai 😭'])}"); return
    if action=="rps":
        bc=random.choice(["rock","paper","scissors"]); win=(text=="rock" and bc=="scissors") or (text=="paper" and bc=="rock") or (text=="scissors" and bc=="paper")
        await interaction.response.send_message(f"Tu: {text} | Bot: {bc}\n{'Jeet gaya! 🔥' if win else 'Haar gaya 💀' if text!=bc else 'Draw! 🤝'}"); return
    if action=="say": await interaction.response.send_message(f"📢 {text}"); return
    if action=="ship":
        per=random.randint(0,100); await interaction.response.send_message(f"💘 {interaction.user.mention} + {u.mention} = **{per}%** {'PERFECT JODI! 😍🔥' if per>80 else 'Chalega 😅'}"); return
    if action=="howgay": await interaction.response.send_message(f"🌈 {u.mention} is **{random.randint(0,100)}%** gay! 😂"); return
    await interaction.response.send_message("Use: meme / joke / 8ball / coinflip / dice / roast / rps / say / ship / howgay")

@bot.tree.command(name="eco", description="Economy - balance, daily, work, beg, pay, rob, slots, gamble, leaderboard")
async def eco(interaction: discord.Interaction, action: str, amount: int = 0, user: discord.Member = None):
    uid=str(interaction.user.id); d=get_eco(uid)
    if action=="balance": await interaction.response.send_message(f"💰 {interaction.user.mention} ke paas **{d['coins']} coins** hai!"); return
    if action=="daily":
        today=datetime.now().strftime("%Y-%m-%d")
        if d["last_daily"]==today: await interaction.response.send_message("❌ Aaj ka le liya! Kal aana!"); return
        amt=random.randint(100,500); d["coins"]+=amt; d["last_daily"]=today; data["eco"][uid]=d; save(); await interaction.response.send_message(f"✅ +{amt} coins! Total: {d['coins']} 💰"); return
    if action=="work":
        amt=random.randint(50,200); d["coins"]+=amt; data["eco"][uid]=d; save(); await interaction.response.send_message(f"💼 +{amt} coins! Total: {d['coins']}"); return
    if action=="beg":
        amt=random.randint(0,100); d["coins"]+=amt; data["eco"][uid]=d; save(); await interaction.response.send_message(f"🥺 {amt} coins mile! Total: {d['coins']}"); return
    if action=="pay":
        if not user: await interaction.response.send_message("❌ User select kar!"); return
        if d["coins"]<amount: await interaction.response.send_message("❌ Coins nahi hai!"); return
        rd=get_eco(user.id); d["coins"]-=amount; rd["coins"]+=amount; data["eco"][uid]=d; data["eco"][str(user.id)]=rd; save(); await interaction.response.send_message(f"✅ {amount} coins {user.mention} ko bhej diye! 💸"); return
    if action=="rob":
        if random.random()<0.5: amt=random.randint(50,200); d["coins"]+=amt; data["eco"][uid]=d; save(); await interaction.response.send_message(f"💀 {amt} coins loot liye! 😈")
        else: await interaction.response.send_message("💀 Pakda gaya! Police aa gayi! 😭"); return
    if action=="slots":
        if d["coins"]<amount: await interaction.response.send_message("❌ Coins nahi hai!"); return
        em=["🍒","🔥","👑","💎","🎰"]; res=[random.choice(em) for _ in range(3)]
        if res[0]==res[1]==res[2]: win=amount*5; d["coins"]+=win; data["eco"][uid]=d; save(); await interaction.response.send_message(f"{' '.join(res)} 🎉 JACKPOT! +{win} coins!")
        else: d["coins"]-=amount; data["eco"][uid]=d; save(); await interaction.response.send_message(f"{' '.join(res)} 💀 Haar gaya! -{amount}"); return
    if action=="gamble":
        if d["coins"]<amount: await interaction.response.send_message("❌ Coins nahi hai!"); return
        if random.random()<0.5: d["coins"]+=amount; data["eco"][uid]=d; save(); await interaction.response.send_message(f"🔥 JEET GAYA! +{amount} Total: {d['coins']}")
        else: d["coins"]-=amount; data["eco"][uid]=d; save(); await interaction.response.send_message(f"💀 HAAR GAYA! -{amount} Total: {d['coins']}"); return
    if action=="leaderboard":
        top=sorted(data["eco"].items(), key=lambda x: x[1]["coins"], reverse=True)[:10]
        txt="".join([f"{i}. <@{uid2}> - {dd['coins']} coins 💰\n" for i,(uid2,dd) in enumerate(top,1)])
        await interaction.response.send_message(f"🏆 **LEADERBOARD**\n{txt or 'Koi nahi!'}"); return
    await interaction.response.send_message("Use: balance / daily / work / beg / pay / rob / slots / gamble / leaderboard")

@bot.tree.command(name="rank", description="Apna level dekh")
async def rank(interaction: discord.Interaction, user: discord.Member = None):
    user=user or interaction.user; lvl=data["levels"].get(str(user.id), {"xp":0,"level":1})
    await interaction.response.send_message(f"⭐ {user.mention} - **Level {lvl['level']}** | XP: {lvl['xp']}/{lvl['level']*100} 🔥")

@bot.tree.command(name="leaderboard", description="Top level wale")
async def lb(interaction: discord.Interaction):
    top=sorted(data["levels"].items(), key=lambda x: x[1]["level"], reverse=True)[:10]
    txt="".join([f"{i}. <@{uid}> - Level {d['level']} ⭐\n" for i,(uid,d) in enumerate(top,1)])
    await interaction.response.send_message(f"🏆 **LEVEL LEADERBOARD**\n{txt or 'Koi nahi!'}")

@bot.tree.command(name="mod", description="Mod - kick, ban, unban, timeout, untimeout, clear, warn, warnings, slowmode, lock, unlock, nuke")
async def mod(interaction: discord.Interaction, action: str, user: discord.Member = None, amount: int = 10, reason: str = "No reason"):
    if action=="kick":
        if not interaction.user.guild_permissions.kick_members: await interaction.response.send_message("❌ Permission nahi!"); return
        await user.kick(reason=reason); await interaction.response.send_message(f"✅ {user.mention} kick!"); return
    if action=="ban":
        if not interaction.user.guild_permissions.ban_members: await interaction.response.send_message("❌ Permission nahi!"); return
        await user.ban(reason=reason); await interaction.response.send_message(f"🔨 {user.mention} BAN!"); return
    if action=="unban":
        try: u=await bot.fetch_user(amount); await interaction.guild.unban(u); await interaction.response.send_message(f"✅ {u.name} unban!")
        except: await interaction.response.send_message("❌ Nahi mila!"); return
    if action=="timeout":
        await user.timeout(timedelta(minutes=amount)); await interaction.response.send_message(f"⏰ {user.mention} ko {amount} min timeout!"); return
    if action=="untimeout": await user.timeout(None); await interaction.response.send_message(f"✅ {user.mention} ka timeout hat gaya!"); return
    if action=="clear":
        await interaction.response.defer(); await interaction.channel.purge(limit=amount); await interaction.followup.send(f"✅ {amount} messages delete! 🧹"); return
    if action=="warn":
        uid=str(user.id); data["warns"][uid]=data["warns"].get(uid,0)+1; save(); await interaction.response.send_message(f"⚠️ {user.mention} warn! Total: {data['warns'][uid]} | {reason}"); return
    if action=="warnings": await interaction.response.send_message(f"⚠️ {user.mention} ke **{data['warns'].get(str(user.id),0)}** warns hai!"); return
    if action=="slowmode": await interaction.channel.edit(slowmode_delay=amount); await interaction.response.send_message(f"🐢 Slowmode {amount} sec!"); return
    if action=="lock": await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False); await interaction.response.send_message("🔒 LOCK!"); return
    if action=="unlock": await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True); await interaction.response.send_message("🔓 UNLOCK!"); return
    if action=="nuke":
        new_ch=await interaction.channel.clone(); await interaction.channel.delete(); await new_ch.send("💥 NUKE HO GAYA! ISC ON TOP! 🔥"); return
    await interaction.response.send_message("Use: kick / ban / timeout / clear / warn / slowmode / lock / unlock / nuke")

@bot.tree.command(name="info", description="Info - ping, avatar, userinfo, serverinfo, botinfo, membercount")
async def info(interaction: discord.Interaction, action: str, user: discord.Member = None):
    u=user or interaction.user
    if action=="ping": await interaction.response.send_message(f"PONG BROTHA!!! 🏓🔥 `{round(bot.latency*1000)}ms`"); return
    if action=="avatar":
        e=discord.Embed(title=f"{u.name} ka Avatar", color=0x00FFFF); e.set_image(url=u.display_avatar.url); await interaction.response.send_message(embed=e); return
    if action=="userinfo":
        e=discord.Embed(title=u.name, color=0xFF00FF); e.add_field(name="ID", value=u.id); e.add_field(name="Joined", value=u.joined_at.strftime("%d/%m/%Y") if u.joined_at else "N/A"); e.add_field(name="Top Role", value=u.top_role.mention); e.set_thumbnail(url=u.display_avatar.url); await interaction.response.send_message(embed=e); return
    if action=="serverinfo":
        g=interaction.guild; e=discord.Embed(title=g.name, color=0x00FF00); e.add_field(name="Members", value=g.member_count); e.add_field(name="Owner", value=g.owner.mention if g.owner else "N/A"); await interaction.response.send_message(embed=e); return
    if action=="botinfo": await interaction.response.send_message(f"👑 **ISC BOT - ISC-ULTRA v2.0**\nServers: {len(bot.guilds)}\nPing: {round(bot.latency*1000)}ms\nISC ON TOP 🔥"); return
    if action=="membercount": await interaction.response.send_message(f"👥 **{interaction.guild.member_count}** brotha hai! 🔥"); return
    await interaction.response.send_message("Use: ping / avatar / userinfo / serverinfo / botinfo / membercount")

@bot.tree.command(name="poll", description="Poll banao")
async def poll(interaction: discord.Interaction, question: str):
    e=discord.Embed(title="📊 POLL", description=question, color=0xFFD700); await interaction.response.send_message(embed=e)
    msg=await interaction.original_response(); await msg.add_reaction("✅"); await msg.add_reaction("❌")

@bot.tree.command(name="announce", description="Announcement")
async def announce(interaction: discord.Interaction, text: str):
    e=discord.Embed(title="📢 ANNOUNCEMENT", description=text, color=0xFF0000); await interaction.response.send_message(embed=e)

@bot.tree.command(name="giveaway", description="Giveaway")
async def giveaway(interaction: discord.Interaction, prize: str, minutes: int = 1):
    e=discord.Embed(title="🎉 GIVEAWAY!", description=f"Prize: **{prize}**\nReact 🎉 to enter!\nEnds in {minutes} min!", color=0xFF00FF)
    await interaction.response.send_message(embed=e)
    msg=await interaction.original_response(); await msg.add_reaction("🎉")
    await asyncio.sleep(minutes*60)
    msg=await interaction.channel.fetch_message(msg.id)
    users=[u async for u in msg.reactions[0].users() if not u.bot]
    if users: await interaction.channel.send(f"🎉 WINNER: {random.choice(users).mention} ne **{prize}** jeeta! 🔥👑")
    else: await interaction.channel.send("💀 Koi enter nahi hua!")

@bot.tree.command(name="ticket", description="Ticket kholo")
async def ticket(interaction: discord.Interaction, reason: str):
    guild=interaction.guild; overwrites={guild.default_role: discord.PermissionOverwrite(view_channel=False), interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)}
    ch=await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites)
    await ch.send(f"🎫 Ticket by {interaction.user.mention}\nReason: {reason}")
    await interaction.response.send_message(f"✅ Ticket ban gaya: {ch.mention}")

@bot.tree.command(name="suggest", description="Suggestion de")
async def suggest(interaction: discord.Interaction, suggestion: str):
    e=discord.Embed(title="💡 SUGGESTION", description=suggestion, color=0x00FFFF); await interaction.response.send_message(embed=e)

@bot.tree.command(name="afk", description="AFK set kar")
async def afk(interaction: discord.Interaction, reason: str = "AFK hu"):
    await interaction.response.send_message(f"💤 {interaction.user.mention} AFK hai: {reason}")

@bot.tree.command(name="ping", description="Ping check")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"PONG! `{round(bot.latency*1000)}ms` 🔥")

TOKEN=os.getenv("TOKEN")
bot.run(TOKEN)
