import discord
from discord.ext import commands
from discord import Embed
import praw
from prawcore import NotFound
import random
from time import sleep
import requests
import os
import datetime

discord_token = ""  # insert your discord token here

reddit = praw.Reddit()  # authentication for reddit, for more info see
# https://praw.readthedocs.io/en/latest/getting_started/authentication.html

client = commands.Bot(command_prefix='!', self_bot=True)

subreddit_list = []

log_channels = []
log_file = None

deleting = False

end_of_message = ''

magic_ball_answers = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes — definitely',
                      'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Signs point to yes',
                      'Yes', 'Don’t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good',
                      'Very doubtful']


def is_existing(subreddit):
    exists = True
    try:
        reddit.subreddits.search_by_name(subreddit, exact=True)
    except NotFound:
        exists = False
    return exists


@client.event
async def on_ready():
    """
    Called when the client is done preparing the data received from Discord. Usually after login is successful and the
    Client.guilds and co. are filled up.
    """
    print("Launched a bot")


@client.event
async def on_message(message):
    """
    Called when a message is created and sent. This requires Intents.messages to be enabled.

    :param message: new message
    :type message: discord.Message
    """
    if message.author == client.user and message.content and message.content[0] != '!':
        await message.edit(content=f'{message.content} \n{end_of_message}')
    if message.channel in log_channels:
        log_file.write(
            f'server: {message.guild}, channel: {message.channel}, author: {message.author},time: {message.created_at}, message:\n{message.content}\n')
    await client.process_commands(message)


@client.event
async def on_message_delete(message):
    """
    Called when a message is deleted.
    If the message is not found in the internal message cache, then this event will not be called.
    Messages might not be in cache if the message is too old or the client is participating in high traffic guilds.

    :param message: deleted message
    :type message: discord.Message
    """
    if not deleting and len(message.embeds) == 0 and not message.content.startswith('!'):
        embed = Embed(title=f'Message by {message.author} was deleted', description=f'message: \n {message.content}')
        await message.channel.send(embed=embed)


@client.command()
async def say(ctx, *, content):
    """
    Send embed message with content

    First we delete 1 message (with command !say).
    Then we send embed message with content.

    Example of usage: !say test

    :param content: content of embed message,which you want to send in ctx.channel
    :type content: str
    """
    await ctx.channel.purge(limit=1)
    embed = discord.Embed(description=content)
    await ctx.send(embed=embed)


@client.command()
async def delete(ctx, how_many_messages_delete):
    """
    Delete messages from ctx.channel

    We set deleting to True, so discord-self-bot doesn't send messages about deleting messages (on_message_delete event) and then
    delete messages from ctx.channel after this we set deleting to False

    Example of usage: !delete 100

    :param how_many_messages_delete: number of messages to delete
    :type how_many_messages_delete: str
    """
    global deleting
    deleting = True
    await ctx.channel.purge(limit=int(how_many_messages_delete) + 1)
    deleting = False


@client.command()
async def ping(ctx, *, ping_of_user):
    """
    Spam 10000 messages with ping_of_user

    Discord has limit to 2000 chars in message,so we calculate how many pings we can send in one message and then
    we spam messages in ctx.channel with ping_of_user

    Example of usage: !ping @test

    :param ping_of_user: ping of user
    :type ping_of_user: str
    """
    string_of_pings = (2000 // len(str(ping_of_user) + '\n')) * str(ping_of_user) + '\n'
    for i in range(10000):
        await ctx.send(string_of_pings)


@client.command()
async def math(ctx, *, expression):
    """
    Evaluate math expression

    We evaluate expression, then check if len of message > 2000, and then send result or result[:2000] depending on len
    of message.

    Eval is dangerous for public bots, for more info see this article
    https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html

    Example of usage: !math 2 * 2

    :param expression: math expression
    :type expression: str
    """
    result = str(eval(expression))
    if len(result) > 2000:  # length of discord messages must be lower than 2000
        await ctx.send(embed=Embed(description=f'First 2000 digits of {expression} = {result[:2000]}'))
    else:
        await ctx.send(embed=Embed(description=f'{expression} = {result}'))


@client.command()
async def check_reddit(ctx):
    """
    Check for new submissions for all subreddits in subreddit_list

    You should restart discord-self-bot for stop checking, also you can't use other commands, while checking
    """
    if subreddit_list:
        subreddit = reddit.subreddit('+'.join(subreddit_list))
        for submission in subreddit.stream.submissions(skip_existing=True):
            await ctx.send(Embed(image=submission.url))


@client.command()
async def add_subreddit(ctx, *, subredit):
    """
    Add new subreddit to subreddit_list

    Example of usage: !add_subreddit worldnews

    :param subredit: name of subreddit we want to add to our subreddit_list
    :type subredit: str
    """
    global subreddit_list
    if is_existing(subredit) and subredit not in subreddit_list:
        subreddit_list.append(subredit)
        await ctx.send(embed=Embed(description=f'Successful added r/{subredit} in list of subreddits'))
    elif subredit in subreddit_list:
        await ctx.send(embed=Embed(description=f"r/{subredit} already in list of subreddits"))
    else:
        await ctx.send(embed=Embed(description="This subreddit doesn't exist"))


@client.command()
async def delete_subreddit(ctx, *, subreddit):
    """
    Delete subreddit from subreddit_list

    Example of usage: !delete_subreddit savedyouaclick

    :type subreddit: str
    :param subreddit: name of subreddit we want to delete from our subreddit_list
    """
    global subreddit_list
    if subreddit in subreddit_list:
        subreddit_list.remove(subreddit)
        await ctx.send(embed=Embed(description="Subreddit deleted from list of subreddits"))
    else:
        await ctx.send('Subreddit is not in list of subreddits')


@client.command()
async def show_subreddits(ctx):
    """
    Send embed with all subreddits in subreddit_list
    """
    if subreddit_list:  # if subreddit list means if subbredit_list is not empty
        await ctx.send(embed=Embed(description=', '.join(subreddit_list)))
    else:
        await ctx.send(embed=Embed(description='List of subreddits is empty'))


@client.command()
async def clear_list_of_subreddits(ctx):
    """
    Delete all subreddits from subreddit_list
    """
    length = len(subreddit_list)
    subreddit_list.clear()
    await ctx.send(embed=Embed(description=f'List of subreddits cleared, {length} subreddits deleted'))


@client.command()
async def magic_ball(ctx):
    """
    Send random answer from magic_ball_answers
    """
    answer = random.choice(magic_ball_answers)
    await ctx.send(embed=Embed(description=answer))


@client.command()
async def start_log(ctx):
    """
    Start logging and open text file for saving messages to it
    """
    global log_file
    log_file = open('logs.txt', 'w', encoding='utf-8')
    await ctx.send(embed=Embed(description='Start logging'))


@client.command()
async def add_log_channel(ctx):
    """
    Add ctx.channel to log_channels
    """
    log_channels.append(ctx.channel)
    await ctx.send(embed=Embed(description='Added new channel for logging'))


@client.command()
async def stop_log(ctx):
    """
    Stop logging and close log_file
    """
    log_file.close()
    log_channels.clear()
    await ctx.send(embed=Embed(description='Stopped logging, sending logs'))
    await ctx.send(file=discord.File(fp='logs.txt', filename='logs.txt'))


@client.command()
async def server_info(ctx):
    """
    Send info about ctx.guild
    """
    server = ctx.guild
    channels = ', '.join(map(str, server.channels))
    categories = ', '.join(map(str, server.categories))
    icon_url = server.icon_url
    invites = await ctx.guild.invites()
    info_string = f"afk channel: {server.afk_channel} \n" \
                  f"afk timeout: {server.afk_timeout} seconds \n" \
                  f"bitrate limit: {server.bitrate_limit} \n" \
                  f"categories: {categories} \n" \
                  f"channels: {channels} \n" \
                  f"created at: {server.created_at} \n" \
                  f"default role: {server.default_role} \n" \
                  f"description: {server.description} \n" \
                  f"emoji limit: {server.emoji_limit} \n" \
                  f"file size limit: {server.filesize_limit // 1048576} mb \n" \
                  f"id: {server.id} \n" \
                  f"totally members: {server.member_count} \n" \
                  f"name: {server.name} \n" \
                  f"owner id: {server.owner_id} \n" \
                  f"local language: {server.preferred_locale} \n" \
                  f"booster role: {server.premium_subscriber_role} \n" \
                  f"totally boosters: {server.premium_subscription_count} \n" \
                  f"server boost level: {server.premium_tier} \n" \
                  f"updates channel: {server.public_updates_channel} \n" \
                  f"rules channel: {server.rules_channel} \n" \
                  f"verification level: {server.verification_level} \n" \
                  f"invites: {len(invites)} \n" \
                  f"icon of server:\n"
    embed = Embed(description=info_string, title=f'Information about {server}', color=0xd252e3)
    embed.set_image(url=str(icon_url))
    await ctx.send(embed=embed)


@client.command()
async def change_presence(ctx, *, presence):
    """
    Changes the client’s presence

    Example of usage: !change_presence test|test

    :param presence: string, which contains presence and details split by |
    :type presence: str
    """
    array_of_presence_and_details = presence.split('|')
    name = array_of_presence_and_details[0]
    details = ''
    if len(array_of_presence_and_details) == 2:
        details = array_of_presence_and_details[1]

    activity = discord.Activity(name=name, type=discord.ActivityType.playing, details=details)

    await client.change_presence(activity=activity)
    await ctx.send(embed=Embed(description='presence successfully changed'))


@client.command()
async def add_ending(ctx, *, message_ending=''):
    """
    Change message ending
    If you want to reset message_ending use !add_ending without arguments

    Example of usage: !add_ending test

    Example for reset: !add_ending

    :param message_ending: ending of message you want
    :type message_ending: str
    """
    global end_of_message
    end_of_message = message_ending
    await ctx.send(embed=Embed(description='ending successfully changed'))


@client.command()
async def emojis(ctx):
    emoji_list = [
        ':grinning:',
        ':heart_eyes:',
        ':rage:',
        ':hot_face:',
        ':cold_face:',
        ':scream:',
        ':smiling_imp:',
        ':sunglasses:',
        ':poop:',
        ':star_struck:',
        ':partying_face:',
        ':exploding_head:',
        ':kissing_heart:',
        ':clown:',
        ':alien:',
    ]

    for emoji in emoji_list:
        await ctx.message.edit(content=emoji)
        sleep(1)

@client.command()
async def cat(ctx):
    "Get fake cat photo from 'https://thiscatdoesnotexist.com/'"
    image = requests.get('https://thiscatdoesnotexist.com/')

    file = open('cat.jpg', 'wb')
    file.write(image.content)
    file.close()

    await ctx.send(file=discord.File('cat.jpg'))

    os.remove('cat.jpg')


@client.command()
async def horse(ctx):
    "Get fake horse photo from https://thishorsedoesnotexist.com"
    image = requests.get('https://thishorsedoesnotexist.com')

    file = open('horse.jpg', 'wb')
    file.write(image.content)
    file.close()

    await ctx.send(file=discord.File('horse.jpg'))

    os.remove('horse.jpg')


@client.command()
async def person(ctx):
    "Get fake peson photo from https://thispersondoesnotexist.com"
    image = requests.get('https://thispersondoesnotexist.com/image')

    file = open('person.jpg', 'wb')
    file.write(image.content)
    file.close()

    await ctx.send(file=discord.File('person.jpg'))

    os.remove('person.jpg')


@client.command()
async def timer(ctx, seconds):
    "Creates messagr-timer and updates it"
    seconds = int(seconds)
    start = datetime.datetime.now()
    finish = start + datetime.timedelta(seconds=seconds)
    difference = finish - start

    while difference.total_seconds() > 0:
        current = datetime.datetime.now()
        difference = finish - current
        await ctx.message.edit(embed=Embed(
            description=f'You have {difference.days} days, {int(difference.total_seconds() // 3600 % 24)} hours, {int(difference.total_seconds() // 60 % 60)} minutes, {difference.seconds % 60} seconds left'))
        sleep(1)

    await ctx.message.delete()

client.run(discord_token, bot=False)
