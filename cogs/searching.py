from discord.ext import commands
import requests
import googlesearch
from bs4 import BeautifulSoup
import re
import discord
from decouple import config
from random import randint

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def google(self, ctx, *, search='stack overflow'):
        """
        Get the first result of google search
        Example of usage: !google test
        """
        result = googlesearch.search(search, num_results=1)
        await ctx.send(result[0])

    @commands.command()
    async def youtube(self, ctx, *, search='unravel'):
        """
        Get first video from youtube search
        Example of usage: !youtube test
        """
        site = requests.get(f"https://www.youtube.com/results?search_query={search.replace(' ', '+')}")

        link_to_video = re.search('/watch\\?v=[\\w]+', site.text)

        await ctx.send(f'First result of search on youtube \n https://www.youtube.com{link_to_video.group()}')

    @commands.command()
    async def github(self, ctx, *, search='svorogaze'):
        """
        Get first repo from search
        Example of usage: !github discord.py
        """
        bs = create_bs(f"https://github.com/search?q={search.replace(' ', '+')}")

        first_repo = bs.find('a', class_='v-align-middle')

        await ctx.send(f"First result of search on github \n https://github.com{first_repo['href']}")

    @commands.command()
    async def covid(self, ctx):
        """
        Get stats of covid for US
        """
        bs = create_bs('https://covidusa.net/')

        total_cases = bs.find('div', class_='stat-value display-4 text-warning').contents[0]
        total_deaths = bs.find('div', class_='stat-value display-4 text-danger').contents[0]

        embed = discord.Embed()
        embed.add_field(name='Total cases in US', value=total_cases, inline=False)
        embed.add_field(name='Total deaths in US', value=total_deaths, inline=False)

        await ctx.send(embed=embed)
   
    @commands.command()
    async def gif_search(self, ctx, *, search='cat'):
        """
        Search giphy for gifs and send one of them
        """
        url = f"http://api.giphy.com/v1/gifs/search?q={search.replace(' ', '+')}&api_key={config('GIPHY_API_KEY')}"
        response = requests.get(url)

        list_of_gifs = response.json()['data']
        random_gif = list_of_gifs[randint(0, len(list_of_gifs) - 1)]

        await ctx.send(random_gif['url'])

def setup(bot):
    bot.add_cog(Search(bot))


def create_bs(link_to_site):
    site = requests.get(link_to_site)
    bs = BeautifulSoup(site.text, 'html.parser')
    return bs
