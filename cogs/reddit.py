from discord.ext import commands
import discord
import praw
from prawcore import NotFound


class RedditBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.subreddit_list = []

    @commands.command()
    async def check_reddit(self, ctx):
        """
        Check for new submissions for all subreddits in subreddit_list

        You should restart discord-self-bot for stop checking, also you can't use other commands, while checking
        """
        if self.subreddit_list:
            subreddit = reddit.subreddit('+'.join(self.subreddit_list))
            for submission in subreddit.stream.submissions(skip_existing=True):
                await ctx.send(discord.Embed(image=submission.url))

    @commands.command()
    async def add_subreddit(self, ctx, *, subredit):
        """
        Add new subreddit to subreddit_list

        Example of usage: !add_subreddit worldnews

        :param subredit: name of subreddit we want to add to our subreddit_list
        :type subredit: str
        """
        if is_existing(subredit) and subredit not in self.subreddit_list:
            self.subreddit_list.append(subredit)
            await ctx.send(embed=discord.Embed(description=f'Successful added r/{subredit} in list of subreddits'))
        elif subredit in self.subreddit_list:
            await ctx.send(embed=discord.Embed(description=f"r/{subredit} already in list of subreddits"))
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
        if self.subreddit_list:  # if subreddit list means if subbredit_list is not empty
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


def is_existing(subreddit):
    exists = True
    try:
        reddit.subreddits.search_by_name(subreddit, exact=True)
    except NotFound:
        exists = False
    return exists


reddit = praw.Reddit() # authentication for reddit, for more info see
# https://praw.readthedocs.io/en/latest/getting_started/authentication.html


def setup(bot):
    bot.add_cog(RedditBot(bot))
