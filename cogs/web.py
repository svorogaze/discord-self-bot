from discord.ext import commands
import discord
import os
import requests
import googlesearch
import random


class Web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        """
        Get fake cat photo from 'https://thiscatdoesnotexist.com/'
        """
        image = requests.get('https://thiscatdoesnotexist.com/')

        file = open('cat.jpg', 'wb')
        file.write(image.content)
        file.close()

        await ctx.send(file=discord.File('cat.jpg'))

        os.remove('cat.jpg')

    @commands.command()
    async def horse(self, ctx):
        """
        Get fake horse photo from https://thishorsedoesnotexist.com
        """

        image = requests.get('https://thishorsedoesnotexist.com')

        file = open('horse.jpg', 'wb')
        file.write(image.content)
        file.close()

        await ctx.send(file=discord.File('horse.jpg'))

        os.remove('horse.jpg')

    @commands.command()
    async def person(self, ctx):
        """
        Get fake peson photo from https://thispersondoesnotexist.com
        """
        image = requests.get('https://thispersondoesnotexist.com/image')

        file = open('person.jpg', 'wb')
        file.write(image.content)
        file.close()

        await ctx.send(file=discord.File('person.jpg'))

        os.remove('person.jpg')

    @commands.command()
    async def waifu(self, ctx):
        """
        This site generate image link like this www.thiswaifudoesnotexist.net/example-' + id + '.jpg'
        id is random number from 0 to 100000
        """
        image = requests.get(f'https://www.thiswaifudoesnotexist.net/example-{random.randint(0, 100000)}.jpg')
        file = open('waifu.jpg', 'wb')
        file.write(image.content)
        file.close()

        await ctx.send(file=discord.File('waifu.jpg'))

        os.remove('waifu.jpg')

    @commands.command()
    async def google(self, ctx, search):
        """
        Get the first result of google search
        """
        result = googlesearch.search(search, num_results=1)
        await ctx.send(result[0])


def setup(bot):
    bot.add_cog(Web(bot))
