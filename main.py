import discord
from dotenv import load_dotenv
import os

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


@bot.tree.command(name='back_to_top',description='返回首条消息的链接')
async def back_to_top(interaction: discord.Interaction):
    async for mess in interaction.channel.history(limit=1, oldest_first=True):
        link = mess.jump_url
    await interaction.response.send_message(link)


bot.run(TOKEN)
