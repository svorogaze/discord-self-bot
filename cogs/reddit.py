import discord
from discord.ext import commands
from decouple import config
import asyncpraw
from asyncprawcore import NotFound


class RedditBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.subreddit_list = []
        self.checking = False

    @commands.command()
    async def check_reddit(self, ctx):
        """
        Check for new submissions for all subreddits in subreddit_list
        """
        self.checking = True
        if self.subreddit_list:
            subreddit = await reddit.subreddit('+'.join(self.subreddit_list))
            async for submission in subreddit.stream.submissions(skip_existing=True):
                if not self.checking:
                    break
                await ctx.send(f"New post in r/{submission.subreddit.display_name} \n {submission.url}")

    @commands.command()
    async def stop_checking(self, ctx):
        """
        Stop checking reddit
        """
        self.checking = False
        await ctx.send('successfully stopped the reddit checking')

    @commands.command()
    async def add_subreddit(self, ctx, *, subreddit):
        """
        Add new subreddit to subreddit_list

        Example of usage: !add_subreddit worldnews

        :param subreddit: name of subreddit we want to add to our subreddit_list
        :type subreddit: str
        """
        if is_exists(subreddit) and subreddit not in self.subreddit_list:
            self.subreddit_list.append(subreddit)
            await ctx.send(embed=discord.Embed(description=f'Successful added r/{subreddit} in list of subreddits'))
        elif subreddit in self.subreddit_list:
            await ctx.send(embed=discord.Embed(description=f"r/{subreddit} already in list of subreddits"))
        else:
            await ctx.send(embed=discord.Embed(description="This subreddit doesn't exist"))

    @commands.command()
    async def delete_subreddit(self, ctx, *, subreddit):
        """
        Delete subreddit from subreddit_list

        Example of usage: !delete_subreddit savedyouaclick

        :type subreddit: str
        :param subreddit: name of subreddit we want to delete from our subreddit_list
        """
        if subreddit in self.subreddit_list:
            self.subreddit_list.remove(subreddit)
            await ctx.send(embed=discord.Embed(description="Subreddit deleted from list of subreddits"))
        else:
            await ctx.send('Subreddit is not in list of subreddits')

    @commands.command()
    async def show_subreddits(self, ctx):
        """
        Send embed with all subreddits in subreddit_list
        """
        if self.subreddit_list:  # if subreddit list means if subreddit_list is not empty
            await ctx.send(embed=discord.Embed(description=', '.join(self.subreddit_list)))
        else:
            await ctx.send(embed=discord.Embed(description='List of subreddits is empty'))

    @commands.command()
    async def clear_list_of_subreddits(self, ctx):
        """
        Delete all subreddits from subreddit_list
        """
        length = len(self.subreddit_list)
        self.subreddit_list.clear()
        await ctx.send(embed=discord.Embed(description=f'List of subreddits cleared, {length} subreddits deleted'))

    @commands.command()
    async def subreddit(self, ctx, *, search='savedyouaclick'):
        """
        Get first subreddit from reddit search
        Example of usage: !subreddit savedyouaclick
        """
        async for subreddit in reddit.subreddits.search_by_name(search, exact=False):
            await ctx.send(f'First result of subreddit \n https://www.reddit.com/r/{subreddit.display_name}')
            break

    @commands.command()
    async def random_subreddit(self, ctx):
        """
        Get random subreddit
        """
        subreddit = await reddit.random_subreddit()
        await ctx.send(f'https://www.reddit.com/r/{subreddit.display_name}')


def is_exists(subreddit):
    exists = True
    try:
        reddit.subreddits.search_by_name(subreddit, exact=True)
    except NotFound:
        exists = False
    return exists


def setup(bot):
    bot.add_cog(RedditBot(bot))


reddit = asyncpraw.Reddit(client_id=config('CLIENT_ID'),
                          client_secret=config('CLIENT_SECRET'),
                          password=config('REDDIT_PASSWORD'),
                          user_agent=config('USER_AGENT'),
                          username=config("REDDIT_USERNAME"))  # authentication for reddit, for more info see
# https://praw.readthedocs.io/en/latest/getting_started/authentication.html
