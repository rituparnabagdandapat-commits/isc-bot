import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome-user")
        if channel is None:
            print("Could not find #welcome-user channel!")
            return
        
        embed = discord.Embed(
            title=f"Welcome to {member.guild.name}! 🎉",
            description=f"Hey {member.mention}, welcome to **{member.guild.name}**!\n\nYou are member **#{len(member.guild.members)}**",
            color=0x00ff00
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Enjoy your stay!")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome-user")
        if channel:
            await channel.send(f"Bye bye {member.name}... We will miss you! 👋")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
