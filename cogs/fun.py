import discord
from discord.ext import commands
import cv2
import requests
import random
from time import sleep
import datetime
import os
import googletrans

MAGIC_BALL_ANSWERS = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes — definitely',
                      'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Signs point to yes',
                      'Yes', 'Don’t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good',
                      'Very doubtful']


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, content='Hello World!'):
        """
        Send embed message with content

        First we delete 1 message (with command !say).
        Then we send embed message with content.

        Example of usage: !say test

        :param content: content of embed message,which you want to send in ctx.channel
        :type content: str
        """
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(description=content)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx, *, ping_of_user='test'):
        """
        Spam 10000 messages with ping_of_user

        Discord has limit to 2000 chars in message,so we calculate how many pings we can send in one message and then
        we spam messages in ctx.channel with ping_of_user

        Example of usage: !ping @test

        :param ping_of_user: ping of user
        :type ping_of_user: str
        """
        string_of_pings = (2000 // len(str(ping_of_user) + '\n')) * str(ping_of_user) + '\n'
        for i in range(10000):
            await ctx.send(string_of_pings)

    @commands.command()
    async def spam_work(self, ctx):
        for i in range(10000):
            await ctx.send('!!work')
            sleep(600)
         
    @commands.command()
    async def math(self, ctx, *, expression='2 * 2'):
        """
        Evaluate math expression

        We evaluate expression, then check if len of message > 2000, and then send result or result[:2000] depending on len
        of message.

        Eval is dangerous for public bots, for more info see this article
        https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html

        Example of usage: !math 2 * 2

        :param expression: math expression
        :type expression: str
        """
        result = str(eval(expression))
        if len(result) > 2000:  # length of discord messages must be lower than 2000
            await ctx.send(embed=discord.Embed(description=f'First 2000 digits of {expression} = {result[:2000]}'))
        else:
            await ctx.send(embed=discord.Embed(description=f'{expression} = {result}'))

    @commands.command()
    async def magic_ball(self, ctx):
        """
        Send random answer from magic_ball_answers
        """
        answer = random.choice(MAGIC_BALL_ANSWERS)
        await ctx.send(embed=discord.Embed(description=answer))

    @commands.command()
    async def emojis(self, ctx):
        emoji_list = [
            ':grinning:',
            ':heart_eyes:',
            ':rage:',
            ':hot_face:',
            ':cold_face:',
            ':scream:',
            ':smiling_imp:',
            ':sunglasses:',
            ':poop:',
            ':star_struck:',
            ':partying_face:',
            ':exploding_head:',
            ':kissing_heart:',
            ':clown:',
            ':alien:',
        ]

        for emoji in emoji_list:
            await ctx.message.edit(content=emoji)
            sleep(1)

    @commands.command()
    async def timer(self, ctx, seconds='100'):
        """
        Create message-timer and updates it
        Example of usage: !timer 100
        """

        seconds = int(seconds)
        start = datetime.datetime.now()
        finish = start + datetime.timedelta(seconds=seconds)
        difference = finish - start

        while difference.total_seconds() > 0:
            current = datetime.datetime.now()
            difference = finish - current
            await ctx.message.edit(embed=discord.Embed(
                description=f'You have {difference.days} days, {int(difference.total_seconds() // 3600 % 24)} hours, '
                            f'{int(difference.total_seconds() // 60 % 60)} minutes, {difference.seconds % 60} seconds left')
            )
            sleep(1)

        await ctx.message.delete()

    @commands.command()
    async def gray(self, ctx):
        """
        Download image, grayscale and send it in ctx.channel
        """
        message = ctx.message
        if len(message.attachments) == 1:
            image = requests.get(message.attachments[0].url)

            file = open('image.jpg', 'wb')
            file.write(image.content)
            file.close()

            gray_image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
            cv2.imwrite('image.jpg', gray_image)

            await ctx.send(file=discord.File('image.jpg'))

            os.remove('image.jpg')

    @commands.command()
    async def translate(self, ctx, *, text='東京喰種'):
        """
        Translate word to english
        """
        translator = googletrans.Translator()
        result = translator.translate(text=text)
        await ctx.send(embed=discord.Embed(description=f'{text} ({result.src}) --> {result.text} ({result.dest})'))

    @commands.command()
    async def distance(self, ctx, x1, y1, x2, y2):
        """
        Get distance between two points (x1,y1) and (x2,y2)
        Example of usage !distance 2 2 5 6
        """
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        a = abs(x2) - abs(x1)
        b = abs(y2) - abs(y1)
        distance = (a ** 2 + b ** 2) ** 0.5
        await ctx.send(f'Shortest distance between ({x1}, {y1}) and ({x2}, {y2}) is {distance}')


def setup(bot):
    bot.add_cog(Fun(bot))
