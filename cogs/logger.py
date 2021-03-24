from discord.ext import commands
import discord
from .mod import deleting
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
        if message.channel in self.log_channels:
            self.log_file.write(
                f'server: {message.guild}, channel: {message.channel}, author: {message.author},time: {message.created_at}, message:\n{message.content}\n')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """
        Called when a message is deleted.
        If the message is not found in the internal message cache, then this event will not be called.
        Messages might not be in cache if the message is too old or the client is participating in high traffic guilds.

        :param message: deleted message
        :type message: discord.Message
        """
        if not deleting and len(message.embeds) == 0 and not message.content.startswith('!'):
            embed = discord.Embed(title=f'Message by {message.author} was deleted',
                                  description=f'message: \n {message.content}')
            await message.channel.send(embed=embed)

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
