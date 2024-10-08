import discord
from dotenv import load_dotenv
import os,re,asyncio

from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='%', intents=intents)


env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# 从环境变量中获取 TOKEN
TOKEN = os.getenv('DISCORD_BOT_TOKEN')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    await bot.tree.sync()
# b23
@bot.event
async def on_message(message):
    pattern = r'b23\.tv/\S*'
    match = re.search(pattern, message.content)
    embed = discord.Embed(description=f"{message.author.mention}请不要发送短链接！",color=0xff0000)
    if match:
        await message.delete()
        await message.channel.send(embed=embed, delete_after=2)


@bot.event
async def on_message_edit(before, after):
    pattern = r'b23\.tv/\S*'
    match = re.search(pattern, after.content)
    embed = discord.Embed(description=f"{before.author.mention}请不要发送短链接！",color=0xff0000)
    if match:
        await after.delete()
        await after.channel.send(embed=embed, delete_after=2)



@bot.event
async def on_reaction_add(reaction,user):
    embed=discord.Embed(description=f'{user.mention} added {reaction.emoji} [here]({reaction.message.jump_url})',color=	0x008000)
    guild=bot.get_guild(1252887256327520287)
    log=guild.get_channel(1269303446230798411)
    await log.send(embed=embed)

@bot.event
async def on_reaction_remove(reaction,user):
    embed=discord.Embed(description=f'{user.mention} removed {reaction.emoji} [here]({reaction.message.jump_url})',color=0xff0000)
    guild=bot.get_guild(1252887256327520287)
    log=guild.get_channel(1269303446230798411)
    await log.send(embed=embed)


async def load():
    for filename in os.listdir('./extensions'):
        if filename.endswith('.py'):
            await bot.load_extension(f'extensions.{filename[:-3]}')

async def main():
    await load()


    await bot.start(TOKEN)

asyncio.run(main())
