from discord.ext import commands
import discord
import platform


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.end_of_message = ''

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Called when a message is created and sent. This requires Intents.messages to be enabled.

        :param message: new message
        :type message: discord.Message
        """
        if message.author == self.bot.user and message.content and message.content[0] != '!':
            await message.edit(content=f'{message.content} \n{self.end_of_message}')

    @commands.command()
    async def latency(self, ctx):
        """
        Get latency of client
        """
        await ctx.send(embed=discord.Embed(description=f'Your ping is {round(self.bot.latency * 1000, 2)} ms'))

    @commands.command()
    async def os(self, ctx):
        """
        Display info about your os
        """
        embed = discord.Embed(title='OS information')
        embed.add_field(name='OS', value=platform.system(), inline=False)
        embed.add_field(name='Release', value=platform.release(), inline=False)
        embed.add_field(name='Python version', value=platform.python_version(), inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def change_presence(self, ctx, *, presence='test|test'):
        """
        Changes the client’s presence

        Example of usage: !change_presence test|test

        :param presence: string, which contains presence and details split by |
        :type presence: str
        """
        array_of_presence_and_details = presence.split('|')
        name = array_of_presence_and_details[0]
        details = ''
        if len(array_of_presence_and_details) == 2:
            details = array_of_presence_and_details[1]

        activity = discord.Activity(name=name, type=discord.ActivityType.playing, details=details)

        await self.bot.change_presence(activity=activity)
        await ctx.send(embed=discord.Embed(description='presence successfully changed'))

    @commands.command()
    async def add_ending(self, ctx, *, message_ending=''):

        """
        Change message ending
        If you want to reset message_ending use !add_ending without arguments

        Example of usage: !add_ending test

        Example for reset: !add_ending

        :param message_ending: ending of message you want
        :type message_ending: str
        """

        self.end_of_message = message_ending
        await ctx.send(embed=discord.Embed(description='ending successfully changed'))


def setup(bot):
    bot.add_cog(User(bot))
