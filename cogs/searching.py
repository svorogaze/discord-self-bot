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

    @commands.command()
    async def steam(self, ctx, id):
        """
        Get stats for given steam id 64
        """
        dict_of_personastates = {0: 'offline', 1: 'online', 2: 'busy', 3: 'away', 4: 'snooze', 5: 'looking to trade',
                                 6: 'looking to play'}

        json = requests.get(
            f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={config('STEAM_API_KEY')}&steamids={id}").json()
        data = json['response']['players'][0]

        embed = discord.Embed()
        embed.set_image(url=data['avatarfull'])
        embed.add_field(name='nickname', value=data['personaname'], inline=False)
        embed.add_field(name='real name', value=data.get('realname', 'not given'), inline=False)
        embed.add_field(name='status', value=dict_of_personastates[data['profilestate']], inline=False)
        embed.add_field(name='profile created (in unix)', value=data.get('timecreated', 'not given'), inline=False)
        embed.add_field(name='last logoff (in unix)', value=data.get('lastlogoff', 'not given'), inline=False)
        embed.add_field(name='country code', value=data.get('loccountrycode', 'not given'), inline=False)
        embed.add_field(name='profile url', value=data['profileurl'], inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def csgo(self, ctx, id):
        """
        Get stats in csgo for given steam id 64
        Profile with given id must be public
        """
        json = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={config('STEAM_API_KEY')}&steamid={id}").json()
        stats = json['playerstats']['stats']

        embed = discord.Embed()
        for dict_of_stat in stats:
            stat_name, stat_value = dict_of_stat['name'], dict_of_stat['value']
            stat_value = str(stat_value)
            if len(embed) + len(stat_name) + len(stat_value) >= 2000:
                await ctx.send(embed=embed)
                embed = discord.Embed()
            embed.add_field(name=stat_name, value=stat_value, inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Search(bot))


def create_bs(link_to_site):
    site = requests.get(link_to_site)
    bs = BeautifulSoup(site.text, 'html.parser')
    return bs
