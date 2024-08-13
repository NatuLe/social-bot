from discord.ext import commands
import discord,os
from discord import Interaction,app_commands,Embed,File

class Export(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        
    

    @app_commands.command(
        name="export_posters_messages",
        description="Export the messages from the original poster of current thread.",
        )
    async def export_posters_messages(self, ctx: Interaction):

        await ctx.response.defer()
        channel = ctx.channel
        allowed_channels_ids=[1268262603201839235]
        
        
        try:
            if channel.parent.id in allowed_channels_ids:
                pass
        except:
            await ctx.followup.send(embed=Embed(title="Error", description="You cant use this command here!", color=0xff0000),ephemeral=True)
            return
        init_message = None

        # Get the initial message
        async for message in channel.history(limit=1,oldest_first=True):
            init_message = message

        if not init_message:
            embed = Embed(title="Error", description="This thread doesn't have an initial post.", color=0xff0000)
            await ctx.followup.send(embed=embed, ephemeral=True)
            return

        poster = init_message.author
        messagesofposter = []

        # Collect all messages from the poster
        async for message in channel.history(limit=None):
            if message.author == poster:
                messagesofposter.append(message.content)

        messagesofposter = "\n\n".join(reversed(messagesofposter))
        total_characters = len(messagesofposter)
        # Ensure the directory exists
        directory = "./files"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the messages to a file
        file_path = os.path.join(directory, f"{channel.name}_by_{poster.display_name}.md")
        with open(file_path, "w+") as f:
            f.write(messagesofposter)
        
        # Create and followup.send the success embed
        try:
            embed = Embed(
                title="Export",
                description=f"Exported {total_characters} characters from {poster.mention} to `{channel.name}_by_{poster.display_name}.md`.",
                color=0x00ff00
            )
            
            
            await ctx.followup.send(embed=embed,file=File(fp=file_path))
        except Exception as e:
            await ctx.followup.send(f'{e}')

async def setup(bot):
    await bot.add_cog(Export(bot))