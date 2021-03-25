from discord.ext import commands
import discord
import os
import requests
import googlesearch


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
    async def google(self, ctx, search):
        """
        Get the first result of search
        """
        result = googlesearch.search(search, num_results=1)
        await ctx.send(result[0])


def setup(bot):
    bot.add_cog(Web(bot))
