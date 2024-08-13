import interactions
from interactions import Client,Intents,listen,slash_command,SlashContext
import interactions.api.events as Events
from dotenv import load_dotenv
import os,re



bot = Client(intents=Intents.ALL)


env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# 从环境变量中获取 TOKEN
TOKEN = os.getenv('DISCORD_BOT_TOKEN')


@listen(Events.Ready)
async def on_ready(event):
    print(f'Logged in as {bot.app.name} ')
    print('------')
    
# b23
@listen(Events.MessageCreate)
async def on_message_create(event:Events.MessageCreate):
    message=event.message
    pattern = r'b23\.tv/\S*'
    match = re.search(pattern, message.content)
    embed = interactions.Embed(description=f"{message.author.mention}请不要发送短链接！",color=0xff0000)
    if match:
        await message.delete()
        await message.channel.send(embed=embed, delete_after=2)


@listen(Events.MessageUpdate)
async def on_message_edit(event:Events.MessageUpdate):

    before=event.before
    after=event.after
    pattern = r'b23\.tv/\S*'
    match = re.search(pattern, after.content)
    embed = interactions.Embed(description=f"{before.author.mention}请不要发送短链接！",color=0xff0000)
    if match:
        await after.delete()
        await after.channel.send(embed=embed, delete_after=2)


@listen(Events.MessageReactionAdd)
async def on_reaction_add(event:Events.MessageReactionAdd):
    user=event.author
    reaction=event.emoji
    jump_url=event.message.jump_url
    embed=interactions.Embed(description=f'{user.mention} added {reaction.name} [here]({jump_url})',color=	0x008000)
    guild=bot.get_guild(1252887256327520287)
    log=guild.get_channel(1269303446230798411)
    await log.send(embed=embed)

@listen(Events.MessageReactionRemove)
async def on_reaction_remove(event:Events.MessageReactionRemove):
    user=event.author
    reaction=event.emoji
    jump_url=event.message.jump_url
    embed=interactions.Embed(description=f'{user.mention} removed {reaction.name} [here]({jump_url})',color=0xff0000)
    guild=bot.get_guild(1252887256327520287)
    log=guild.get_channel(1269303446230798411)
    await log.send(embed=embed)




@slash_command(name='back-to-top', description='返回顶部')
async def back_to_top(ctx: SlashContext):
    await ctx.defer()
    channel=ctx.channel
    async for mess in ctx.channel.history(limit=None):
        last_message = mess
    link = last_message.jump_url
    await ctx.respond(content=f'[返回顶部]({link})')

extensions_dir = "extensions"

# Iterate through the files in the extensions directory
for filename in os.listdir(extensions_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        # Construct the module name
        module_name = f"{extensions_dir}.{filename[:-3]}"
        # Load the extension
        bot.load_extension(module_name)


bot.start(TOKEN)


# source myenv/bin/activate