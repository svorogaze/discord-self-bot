from discord.ext import commands
import requests
import googlesearch
from bs4 import BeautifulSoup
import re


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def google(self, ctx, *, search):
        """
        Get the first result of google search
        """
        result = googlesearch.search(search, num_results=1)
        await ctx.send(result[0])

    @commands.command()
    async def youtube(self, ctx, *, search):
        """
        Get first video from youtube search
        """
        site = requests.get(f"https://www.youtube.com/results?search_query={search.replace(' ', '+')}")

        link_to_video = re.search('/watch\\?v=[\\w]+', site.text)

        await ctx.send(f'First result of search on youtube \n https://www.youtube.com{link_to_video.group()}')

    @commands.command()
    async def github(self, ctx, *, search):
        """
        Get first repo from search
        """
        bs = create_bs(f"https://github.com/search?q={search.replace(' ', '+')}")

        first_repo = bs.find('a', class_='v-align-middle')

        await ctx.send(f"First result of search on github \n https://github.com{first_repo['href']}")


def setup(bot):
    bot.add_cog(Search(bot))


def create_bs(link_to_site):
    site = requests.get(link_to_site)
    bs = BeautifulSoup(site.text, 'html.parser')
    return bs
