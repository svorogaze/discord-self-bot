from discord.ext import commands
import discord
import os
import requests
import random
from bs4 import BeautifulSoup


class Web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        """
        Get fake cat photo from 'https://thiscatdoesnotexist.com/'
        """
        image = requests.get('https://thiscatdoesnotexist.com/')

        await save_send_and_delete(image=image, file_name='cat', ctx=ctx)

    @commands.command()
    async def horse(self, ctx):
        """
        Get fake horse photo from https://thishorsedoesnotexist.com
        """

        image = requests.get('https://thishorsedoesnotexist.com')

        await save_send_and_delete(image=image, file_name='horse', ctx=ctx)

    @commands.command()
    async def person(self, ctx):
        """
        Get fake person photo from https://thispersondoesnotexist.com
        """
        image = requests.get('https://thispersondoesnotexist.com/image')

        await save_send_and_delete(image=image, file_name='person', ctx=ctx)

    @commands.command()
    async def waifu(self, ctx):
        """
        Get fake waifu from https://www.thiswaifudoesnotexist.net
        This site generate image link like this www.thiswaifudoesnotexist.net/example-' + id + '.jpg'
        id is random number from 0 to 100000
        """

        image_link = f'https://www.thiswaifudoesnotexist.net/example-{random.randint(0, 100000)}.jpg'

        await ctx.send(image_link)

    @commands.command()
    async def art(self, ctx):
        """
        Get fake art from https://thisartworkdoesnotexist.com/
        """
        image = requests.get('https://thisartworkdoesnotexist.com')

        await save_send_and_delete(image=image, file_name='art', ctx=ctx)

    @commands.command()
    async def word(self, ctx):
        """
        Get fake word from https://www.thisworddoesnotexist.com/
        """
        bs = create_bs('https://www.thisworddoesnotexist.com/')

        word = bs.find('div', id='definition-word')
        meaning = bs.find('div', id='definition-definition')

        embed = discord.Embed()
        embed.add_field(name='word: ', value=word.contents[0], inline=False)
        embed.add_field(name='meaning: ', value=meaning.contents[0], inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def eye(self, ctx):
        """
        Get fake eye from https://thiseyedoesnotexist.com
        """
        image_link = f"https://thiseyedoesnotexist.com/{get_static_link_to_img('https://thiseyedoesnotexist.com/random')}"

        await ctx.send(image_link)

    @commands.command()
    async def mp(self, ctx):
        """
        Get fake eye from https://vole.wtf/this-mp-does-not-exist/
        This site has hardcoded 649 images into html, bruh
        """
        image_link = f'https://vole.wtf/this-mp-does-not-exist/mp/mp00{random.randint(0, 649)}.jpg'

        await ctx.send(image_link)

    @commands.command()
    async def city(self, ctx):
        """
        Get fake city from http://thiscitydoesnotexist.com/
        """
        image_link = f"http://thiscitydoesnotexist.com/{get_static_link_to_img('http://thiscitydoesnotexist.com/')}"

        await ctx.send(image_link)

    @commands.command()
    async def sky(self, ctx):
        """
        Get fake sky from https://arthurfindelair.com/thisnightskydoesnotexist/
        Link to image is like this https://firebasestorage.googleapis.com/v0/b/thisnightskydoesnotexist.appspot.com/o/images%2Fseed0001.jpg?alt=media
        """
        image_link = f"https://firebasestorage.googleapis.com/v0/b/thisnightskydoesnotexist.appspot.com/o/images%2Fseed" \
                     f"{'{:0>4d}'.format(random.randint(1, 5000))}.jpg?alt=media"

        await ctx.send(image_link)

    @commands.command()
    async def vessel(self, ctx):
        """
        Get fake vessel from https://thisvesseldoesnotexist
        Link to image is like this https://thisvesseldoesnotexist.s3-us-west-2.amazonaws.com/public/v2/fakes/0009999.jpg
        """
        image_link = f"https://thisvesseldoesnotexist.s3-us-west-2.amazonaws.com/public/v2/fakes/{'{:0>7d}'.format(random.randint(1, 20000))}.jpg"

        await ctx.send(image_link)

    @commands.command()
    async def startup(self, ctx):
        """
        Get fake startup from https://thisstartupdoesnotexist.com/
        """
        bs = create_bs('https://thisstartupdoesnotexist.com/')

        startup = bs.find('h1', class_='theme-title logo-font')
        slogan = bs.find('span', class_='sub-title')

        embed = discord.Embed()
        embed.add_field(name='startup: ', value=startup.contents[0], inline=False)
        embed.add_field(name='slogan: ', value=slogan.contents[0], inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def fu_homer(self, ctx):
        """
        Get a fucked up homer from https://www.thisfuckeduphomerdoesnotexist.com/
        """
        image_link = get_static_link_to_img('https://www.thisfuckeduphomerdoesnotexist.com/')
        await ctx.send(image_link)

    @commands.command()
    async def snack(self, ctx):
        """
        Get name of a fake snack from https://thissnackdoesnotexist.com/
        """
        bs = create_bs('https://thissnackdoesnotexist.com/')

        snack_name = bs.find(name='h1', class_="snack-description")

        await ctx.send(snack_name.contents[0])

    @commands.command()
    async def dad_joke(self, ctx):
        """
        Get fake dad joke from https://icanhazdadjoke.com/
        """
        bs = create_bs('https://icanhazdadjoke.com/')

        dad_joke = bs.find(name='p', class_='subtitle').contents[0]

        await ctx.send(dad_joke)

    @commands.command()
    async def insp_img(self, ctx):
        """
        Get fake inspiration image from https://inspirobot.me/api?generate=true
        """
        image_link = requests.get('https://inspirobot.me/api?generate=true').text

        await ctx.send(image_link)

    @commands.command()
    async def pizza(self, ctx):
        """
        Get fake pizza from https://boredhumans.com/pizza.php
        """
        image_link = f'https://boredhumans.b-cdn.net/pizza/{random.randint(1, 6000)}.jpg'

        await ctx.send(image_link)

    @commands.command()
    async def blended_photo(self, ctx):
        """
        Get blended photo from https://boredhumans.com/photo_blender.php
        """
        image_link = f'https://boredhumans.b-cdn.net/photo_blender/{random.randint(1, 999)}.jpg'

        await ctx.send(image_link)

    @commands.command()
    async def dream(self, ctx):
        """
        Get a fake photo of dream from https://boredhumans.com/dreams.php
        """
        image_link = f'https://boredhumans.b-cdn.net/dreams/{random.randint(1, 125)}.jpg'

        await ctx.send(image_link)

    @commands.command()
    async def scp(self, ctx):
        """
        Get link to random scp from http://www.scpwiki.com
        """
        link_to_scp = f"http://www.scpwiki.com/scp-{'{:0>3d}'.format(random.randint(1, 5199))}"

        await ctx.send(link_to_scp)


def setup(bot):
    bot.add_cog(Web(bot))


def get_static_link_to_img(site_name):
    bs = create_bs(site_name)

    static_link_to_image = bs.find('img')['src']
    return static_link_to_image


async def save_send_and_delete(image, file_name, ctx):
    file = open(f'{file_name}.jpg', 'wb')
    file.write(image.content)
    file.close()

    await ctx.send(file=discord.File(f'{file_name}.jpg'))

    os.remove(f'{file_name}.jpg')


def create_bs(link_to_site):
    site = requests.get(link_to_site)
    bs = BeautifulSoup(site.text, 'html.parser')
    return bs
