from discord.ext import commands
import os

discord_token = ""  # insert your discord token here

self_bot = commands.Bot(command_prefix='!', self_bot=True)

for filename in os.listdir('./cogs'):  # get all cogs in cogs
    if filename.endswith('.py'):
        self_bot.load_extension(f'cogs.{filename[:-3]}')


@self_bot.event
async def on_ready():
    """
    Called when the client is done preparing the data received from Discord. Usually after login is successful and the
    Client.guilds and co. are filled up.
    """
    print("Launched a bot")


self_bot.run(discord_token, bot=False)
