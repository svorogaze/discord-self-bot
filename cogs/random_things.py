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


def setup(bot):
    bot.add_cog(RandomThings(bot))
