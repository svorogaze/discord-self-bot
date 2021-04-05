import discord
from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.list_of_bad_words = []

    @commands.command()
    async def delete(self, ctx, how_many_messages_delete='100'):
        """
        Delete messages from ctx.channel

        We set deleting to True, so discord-self-bot doesn't send messages about deleting messages (on_message_delete event) and then
        delete messages from ctx.channel after this we set deleting to False

        Example of usage: !delete 100

        :param how_many_messages_delete: number of messages to delete
        :type how_many_messages_delete: str
        """
        await ctx.channel.purge(limit=int(how_many_messages_delete) + 1)

    @commands.command()
    async def add_bad_word(self, ctx, bad_word='bad'):
        """
        Example of usage: !add_bad_word bruh
        """
        self.list_of_bad_words.append(bad_word)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            for bad_word in self.list_of_bad_words:
                if bad_word in message.content:
                    await message.reply(
                        embed=discord.Embed(description=f"Hey, we don't say {bad_word} here", color=WARNING_COLOR))


WARNING_COLOR = 0xe81031


def setup(bot):
    bot.add_cog(Mod(bot))
