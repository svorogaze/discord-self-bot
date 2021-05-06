from discord.ext import commands
import discord
import os


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_file = None
        self.log_channels = []

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Called when a message is created and sent. This requires Intents.messages to be enabled.

        :param message: new message
        :type message: discord.Message
        """
        await message.add_reaction(":gorilla:") # just for fun, delete if annoying
        if message.channel in self.log_channels:
            self.log_file.write(
                f'server: {message.guild}, channel: {message.channel}, author: {message.author},time: {message.created_at}, message:\n{message.content}\n')

    @commands.command()
    async def start_log(self, ctx):
        """
        Start logging and open text file for saving messages to it
        """
        self.log_file = open('logs.txt', 'w', encoding='utf-8')
        await ctx.send(embed=discord.Embed(description='Start logging'))

    @commands.command()
    async def add_log_channel(self, ctx):
        """
        Add ctx.channel to log_channels
        """
        self.log_channels.append(ctx.channel)
        await ctx.send(embed=discord.Embed(description='Added new channel for logging'))

    @commands.command()
    async def stop_log(self, ctx):
        """
        Stop logging and close log_file
        """
        self.log_file.close()
        self.log_channels.clear()
        await ctx.send(embed=discord.Embed(description='Stopped logging, sending logs'))
        await ctx.send(file=discord.File(fp='logs.txt', filename='logs.txt'))
        os.remove('logs.txt')


def setup(bot):
    bot.add_cog(Logger(bot))
