import discord
from discord.ext import commands
import asyncio
import os

BOT_ID = 1563112918126698506
SUPPORT_ROLE_ID = 1573558617188073612
TICKET_CATEGORY_NAME = "Tickets"

def _is_support(m):
    if m is None: return False
    if m.guild_permissions.administrator: return True
    return SUPPORT_ROLE_ID in {r.id for r in m.roles}

async def create_ticket(interaction, mode, name, details_text, title):
    guild = interaction.guild
    user = interaction.user
    await interaction.response.defer(ephemeral=True)
    for ch in guild.text_channels:
        if ch.topic and f"owner:{user.id}" in ch.topic and "status:open" in ch.topic:
            await interaction.followup.send(f"You already have an open ticket: {ch.mention}", ephemeral=True)
            return
    cat = discord.utils.get(guild.categories, name=TICKET_CATEGORY_NAME)
    if cat is None:
        cat = await guild.create_category(TICKET_CATEGORY_NAME)
    support_role = guild.get_role(SUPPORT_ROLE_ID)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, attach_files=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_channels=True),
    }
    if support_role:
        overwrites[support_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
    safe = "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-") or "user"
    ch = await guild.create_text_channel(name=f"ticket-{safe}", category=cat, overwrites=overwrites, topic=f"owner:{user.id} | name:{name} | mode:{mode} | status:open")
    if mode == "ai":
        embed = discord.Embed(title="🤖 Support AI - ISC", description=f"Hello **{name}** {user.mention}!\n\nI am <@{BOT_ID}> - Support AI.\n\n{details_text}\n\nType here and I will reply. Want a human? Click **Speak to Support Team** below.", color=0x5865F2)
        await ch.send(embed=embed, view=TicketControlView())
    else:
        embed = discord.Embed(title=f"{title} - ISC", description=f"Hello **{name}** {user.mention}!\n\nSupport Team will help you shortly.\n\n{details_text}", color=0x2b2d31)
        ping = f"{support_role.mention}" if support_role else ""
        await ch.send(content=ping, embed=embed, view=TicketControlView())
    await interaction.followup.send(f"✅ Done! Your private channel: {ch.mention}", ephemeral=True)

class SupportModal(discord.ui.Modal):
    def __init__(self, mode):
        super().__init__(title="Speak to Support Team" if mode=="team" else "Chat with Support AI")
        self.mode = mode
        self.name_input = discord.ui.TextInput(label="What is your name?", placeholder="Write your name...", style=discord.TextStyle.short, max_length=50, required=True)
        self.problem = discord.ui.TextInput(label="What do you need help with?", placeholder="Write your problem...", style=discord.TextStyle.paragraph, max_length=1000, required=True)
        self.add_item(self.name_input); self.add_item(self.problem)
    async def on_submit(self, interaction):
        details = f"**Name:** {self.name_input.value}\n**Problem:** {self.problem.value}"
        await create_ticket(interaction, self.mode, self.name_input.value, details, "👨‍💼 Support Team")

class BugModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Bug Report")
        self.name_input = discord.ui.TextInput(label="What is your name?", placeholder="Your name...", style=discord.TextStyle.short, max_length=50, required=True)
        self.how_found = discord.ui.TextInput(label="How did you find the bug?", placeholder="Where / when did you find it?", style=discord.TextStyle.paragraph, max_length=500, required=True)
        self.what_bug = discord.ui.TextInput(label="What is the bug?", placeholder="Describe the bug in detail...", style=discord.TextStyle.paragraph, max_length=1000, required=True)
        self.media = discord.ui.TextInput(label="Image / Video of the bug", placeholder="Paste link here, or send in ticket after...", style=discord.TextStyle.short, max_length=500, required=False)
        self.add_item(self.name_input); self.add_item(self.how_found); self.add_item(self.what_bug); self.add_item(self.media)
    async def on_submit(self, interaction):
        details = f"**Name:** {self.name_input.value}\n**How found:** {self.how_found.value}\n**What is the bug:** {self.what_bug.value}\n**Image/Video:** {self.media.value or 'Will send in ticket'}"
        await create_ticket(interaction, "bug", self.name_input.value, details, "🐛 Bug Report")

class CreatorModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Content Creator Application")
        self.yt_link = discord.ui.TextInput(label="YT Channel Link?", placeholder="Paste your YouTube channel link...", style=discord.TextStyle.short, max_length=200, required=True)
        self.subs = discord.ui.TextInput(label="Subscriber Count?", placeholder="Ex: 1200", style=discord.TextStyle.short, max_length=20, required=True)
        self.name_input = discord.ui.TextInput(label="What is your Name?", placeholder="Your name...", style=discord.TextStyle.short, max_length=50, required=True)
        self.age = discord.ui.TextInput(label="Age?", placeholder="Ex: 16", style=discord.TextStyle.short, max_length=10, required=True)
        self.rank_lvl = discord.ui.TextInput(label="Rank of Rivals and Lvl?", placeholder="Ex: Diamond 2, Lvl 45", style=discord.TextStyle.short, max_length=100, required=True)
        self.add_item(self.yt_link); self.add_item(self.subs); self.add_item(self.name_input); self.add_item(self.age); self.add_item(self.rank_lvl)
    async def on_submit(self, interaction):
        details = f"**Name:** {self.name_input.value}\n**YT Channel:** {self.yt_link.value}\n**Subscribers:** {self.subs.value}\n**Age:** {self.age.value}\n**Rank of Rivals + Lvl:** {self.rank_lvl.value}"
        await create_ticket(interaction, "creator", self.name_input.value, details, "🎬 Content Creator")

class SupportChoiceView(discord.ui.View):
    def __init__(self): super().__init__(timeout=120)
    @discord.ui.button(label="Speak to a Team", style=discord.ButtonStyle.primary, emoji="👨‍💼", custom_id="support_team")
    async def team_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SupportModal("team"))
    @discord.ui.button(label="Speak to an AI", style=discord.ButtonStyle.success, emoji="🤖", custom_id="support_ai")
    async def ai_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SupportModal("ai"))

class TicketPanelView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Support", style=discord.ButtonStyle.primary, emoji="🛠️", custom_id="panel_support")
    async def support_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Choose who do you want to talk to:", view=SupportChoiceView(), ephemeral=True)
    @discord.ui.button(label="Bug Report", style=discord.ButtonStyle.danger, emoji="🐛", custom_id="panel_bug")
    async def bug_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BugModal())
    @discord.ui.button(label="Content Creator", style=discord.ButtonStyle.success, emoji="🎬", custom_id="panel_creator")
    async def creator_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CreatorModal())

class TicketControlView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Speak to Support Team", style=discord.ButtonStyle.primary, emoji="👨‍💼", custom_id="ticket_to_team")
    async def to_team_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        topic = interaction.channel.topic or ""
        if "mode:ai" in topic:
            await interaction.channel.edit(topic=topic.replace("mode:ai", "mode:team"))
            support_role = interaction.guild.get_role(SUPPORT_ROLE_ID)
            ping = f"{support_role.mention}" if support_role else ""
            await interaction.response.send_message(f"{ping} Moved to Support Team. Human will talk now.", allowed_mentions=discord.AllowedMentions(roles=True))
        else:
            await interaction.response.send_message("Already with Support Team.", ephemeral=True)
    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="ticket_close")
    async def close_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not _is_support(interaction.user):
            await interaction.response.send_message("Only Support Team can close.", ephemeral=True)
            return
        await interaction.response.send_message("Closing in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete(reason=f"Closed by {interaction.user}")

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TicketPanelView())
        self.bot.add_view(TicketControlView())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == BOT_ID: return
        if message.author.bot or not message.guild: return
        topic = message.channel.topic or ""
        is_ticket = message.channel.name.startswith("ticket-") and "status:open" in topic
        if is_ticket and "mode:ai" in topic:
            if _is_support(message.author):
                return
            text = message.content.lower()
            if "human" in text or "staff" in text or "team" in text or "support" in text:
                await message.channel.send("Okay! I will call the Support Team. Click **Speak to Support Team** above.")
            elif "hello" in text or "hi" in text or "hey" in text:
                await message.channel.send(f"Hello {message.author.mention}! I'm Support AI. Tell me your problem.")
            else:
                await message.channel.send("Got it! Can you send more details / screenshot? If you want a human, click **Speak to Support Team**.")

    @discord.app_commands.command(name="add-ticket-panel", description="Send ticket panel in ISC")
    async def add_ticket_panel(self, interaction: discord.Interaction):
        if not _is_support(interaction.user):
            await interaction.response.send_message("Only Support Team.", ephemeral=True)
            return
        embed = discord.Embed(title="🎫 Need Help? - ISC", description="Click an option below:\n\n**🛠️ Support** -> Speak to a Team / Speak to an AI\n**🐛 Bug Report** -> Report a bug\n**🎬 Content Creator** -> Apply for Content Creator\n\nWrite details, press **OK**, private channel will open.", color=0x5865F2)
        await interaction.channel.send(embed=embed, view=TicketPanelView())
        await interaction.response.send_message("Panel setup done! ✅", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
