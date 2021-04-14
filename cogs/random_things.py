from discord.ext import commands
import discord
import requests
import random


class RandomThings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def scp(self, ctx):
        """
        Get link to random scp from http://www.scpwiki.com
        """
        link_to_scp = f"http://www.scpwiki.com/scp-{'{:0>3d}'.format(random.randint(1, 5199))}"

        await ctx.send(link_to_scp)

    @commands.command()
    async def advice(self, ctx):
        """
        Get random advice from https://api.adviceslip.com/advice
        """
        json = requests.get('https://api.adviceslip.com/advice').json()
        await ctx.send(embed=discord.Embed(description=json['slip']['advice'], title='random advice'))

    @commands.command()
    async def cat_fact(self, ctx):
        """
        Get random cat fact from https://meowfacts.herokuapp.com/
        """
        json = requests.get('https://meowfacts.herokuapp.com/').json()
        await ctx.send(embed=discord.Embed(description=json['data'][0], title='random cat fact'))

    @commands.command()
    async def useless_fact(self, ctx):
        """
        Get random useless fact from https://uselessfacts.jsph.pl
        """
        json = requests.get('https://uselessfacts.jsph.pl/random.json?language=en').json()
        await ctx.send(embed=discord.Embed(description=json['text'], title='random useless fact'))

    @commands.command()
    async def fox(self, ctx):
        """
        Get random fox image from https://randomfox.ca
        """
        link = f'https://randomfox.ca/images/{random.randint(1, 122)}.jpg'
        await ctx.send(link)

    @commands.command()
    async def dog(self, ctx):
        """
        Get random dog image from https://dog.ceo/api/breeds/image/random
        """
        json = requests.get('https://dog.ceo/api/breeds/image/random').json()
        await ctx.send(json['message'])


def setup(bot):
    bot.add_cog(RandomThings(bot))
