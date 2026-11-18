import discord
import WelcomeMessage

async def setup(bot):
    @bot.event
    async def on_member_join(member):
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

    @bot.event
    async def on_member_remove(member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome-user")
        if channel:
            await channel.send(f"Bye bye {member.name}... We will miss you! 👋")
