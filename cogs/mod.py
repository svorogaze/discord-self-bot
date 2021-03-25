import discord
from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def delete(self, ctx, how_many_messages_delete):
        """
        Delete messages from ctx.channel

        We set deleting to True, so discord-self-bot doesn't send messages about deleting messages (on_message_delete event) and then
        delete messages from ctx.channel after this we set deleting to False

        Example of usage: !delete 100

        :param how_many_messages_delete: number of messages to delete
        :type how_many_messages_delete: str
        """
        global deleting
        deleting = True
        await ctx.channel.purge(limit=int(how_many_messages_delete) + 1)
        deleting = False


deleting = False


def setup(bot):
    bot.add_cog(Mod(bot))
