from interactions import Extension, slash_command, SlashContext, Embed, File
import os

class Export(Extension):

    @slash_command(
        name="export_posters_messages",
        description="Export the messages from the original poster of current thread.",
        scopes=[1268205038417743923],
    )
    async def export_posters_messages(self, ctx: SlashContext):
        await ctx.defer(ephemeral=True)
        allowed_channels_ids=[1268262603201839235]
        
        channel = ctx.channel
        try:
            if channel.parent_channel.id in allowed_channels_ids:
                pass
        except:
            await ctx.send(embed=Embed(title="Error", description="You cant use this command here!", color=0xff0000),ephemeral=True)
            return
        init_message = None

        # Get the initial message
        async for message in channel.history(limit=None):
            init_message = message

        if not init_message:
            embed = Embed(title="Error", description="This thread doesn't have an initial post.", color=0xff0000)
            await ctx.send(embed=embed, ephemeral=True)
            return

        poster = init_message.author
        messagesofposter = []

        # Collect all messages from the poster
        async for message in channel.history(limit=None):
            if message.author == poster:
                messagesofposter.append(message.content)

        messagesofposter = "\n\n".join(reversed(messagesofposter))

        # Ensure the directory exists
        directory = "./files"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the messages to a file
        file_path = os.path.join(directory, f"{channel.name}_by_{poster.display_name}.md")
        with open(file_path, "w+") as f:
            f.write(messagesofposter)

        # Create and send the success embed
        embed = Embed(
            title="Export",
            description=f"Exported {len(messagesofposter)} characters from {poster.mention} to `{channel.name}_by_{poster.display_name}.md`.",
            color=0x00ff00
        )
        await ctx.send(embed=embed, file=File(file_path))