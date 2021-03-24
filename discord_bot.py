from discord.ext import commands
from cogs import fun, guild, logger, mod, reddit, user, web

discord_token = ""  # insert your discord token here

self_bot = commands.Bot(command_prefix='!', self_bot=True)
self_bot.add_cog(fun.Fun(self_bot))
self_bot.add_cog(guild.Guild(self_bot))
self_bot.add_cog(logger.Logger(self_bot))
self_bot.add_cog(mod.Mod(self_bot))
self_bot.add_cog(reddit.RedditBot(self_bot))
self_bot.add_cog(user.User(self_bot))
self_bot.add_cog(web.Web(self_bot))


@self_bot.event
async def on_ready():
    """
    Called when the client is done preparing the data received from Discord. Usually after login is successful and the
    Client.guilds and co. are filled up.
    """
    print("Launched a bot")


self_bot.run(discord_token, bot=False)
