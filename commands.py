import discord, asyncio, datetime
from discord.ext import commands
from discord import ui

# ---------- TICKET VIEWS ----------
class GameView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label="⛏️ Minecraft", style=discord.ButtonStyle.green, custom_id="game_mc")
    async def mc(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("⛏️ **Minecraft Creator**\n1. Your Minecraft IGN?\n2. YouTube / TikTok link?\n3. Subs? (Need 100+)\n4. Send 1 best video link")
    @ui.button(label="🧱 Roblox", style=discord.ButtonStyle.blurple, custom_id="game_rb")
    async def rb(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("🧱 **Roblox Creator**\n1. Your Roblox Username?\n2. YouTube / TikTok link?\n3. Subs? (Need 100+)\n4. Send 1 best video link")

class CloseView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_btn(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("🔒 Closing in 5s...")
        await asyncio.sleep(5)
        try:
            await interaction.channel.delete()
        except:
            pass

class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    async def create_ticket(self, interaction: discord.Interaction, type_name: str):
        guild = interaction.guild
        cat = discord.utils.get(guild.categories, name="Tickets")
        if not cat:
            cat = await guild.create_category("Tickets")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        ch = await guild.create_text_channel(f"ticket-{type_name}-{interaction.user.name}", category=cat, overwrites=overwrites)
        await interaction.response.send_message(f"Ticket created: {ch.mention}", ephemeral=True)
        if type_name == "creator":
            embed = discord.Embed(title="🎥 Content Creator Application", description=f"{interaction.user.mention}\n\n**Requirement: 100+ Subs!**\nIf less than 100, ticket will be closed.\n\nWhat game do you create for?", color=0x00ff00)
            await ch.send(embed=embed, view=GameView())
            await ch.send("Staff Controls:", view=CloseView())
        elif type_name == "report":
            await ch.send(f"{interaction.user.mention} **🚨 Report**\n1. Who are you reporting? @user\n2. What did they do? + proof screenshot\n3. When did it happen?")
            await ch.send("Staff Controls:", view=CloseView())
        else:
            await ch.send(f"{interaction.user.mention} **🎫 Support**\nWhat do you need help with? Staff will be here soon.")
            await ch.send("Staff Controls:", view=CloseView())
    @ui.button(label="🎫 Support", style=discord.ButtonStyle.grey, custom_id="ticket_support")
    async def support(self, interaction: discord.Interaction, button: ui.Button):
        await self.create_ticket(interaction, "support")
    @ui.button(label="🎥 Content Creator", style=discord.ButtonStyle.green, custom_id="ticket_creator")
    async def creator(self, interaction: discord.Interaction, button: ui.Button):
        await self.create_ticket(interaction, "creator")
    @ui.button(label="🚨 Report", style=discord.ButtonStyle.red, custom_id="ticket_report")
    async def report(self, interaction: discord.Interaction, button: ui.Button):
        await self.create_ticket(interaction, "report")

# ---------- COG ----------
class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # DYNO MOD
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} banned | {reason}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} kicked | {reason}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, seconds: int = 600):
        await member.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=seconds))
        await ctx.send(f"🔇 {member.mention} muted for {seconds}s")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"🧹 Deleted {amount} messages", delete_after=3)

    # /setup-tickets SLASH
    @discord.app_commands.command(name="setup-tickets", description="Setup the ticket panel with 3 buttons")
    @discord.app_commands.describe(channel="Where to send the panel?")
    async def setup_tickets(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Only Admin can do this!", ephemeral=True)
            return
        target = channel or interaction.channel
        embed = discord.Embed(title="🎫 ISC Support", description="Click a button to open a ticket\n\n🎫 **Support** - Need help\n🎥 **Content Creator** - Need 100+ Subs | Minecraft / Roblox\n🚨 **Report** - Report someone", color=0x00ff00)
        await target.send(embed=embed, view=TicketView())
        await interaction.response.send_message(f"Ticket panel sent in {target.mention} ✅", ephemeral=True)

    @discord.app_commands.command(name="close", description="Close this ticket")
    async def close(self, interaction: discord.Interaction):
        if "ticket-" in interaction.channel.name:
            await interaction.response.send_message("🔒 Closing in 5s...")
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("This is not a ticket!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Commands(bot))
