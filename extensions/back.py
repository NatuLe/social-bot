
import discord
from discord.ext import commands
from discord import app_commands
class backtotop(commands.Cog):
    def __init__(self,bot) :
        self.bot=bot
    
    @app_commands.command(name='back_to_top',description='回到顶部')
    async def back_to_top(self,ctx:discord.Interaction):
        await ctx.response.defer()
        async for mess in ctx.channel.history(limit=1, oldest_first=True):
            link = mess.jump_url
        await ctx.followup.send(f'[点击回到顶部]({link})')


async def setup(bot):
    await bot.add_cog(backtotop(bot))