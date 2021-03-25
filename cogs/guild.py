import discord
from discord.ext import commands


class Guild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def server_info(self, ctx):
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
        embed = discord.Embed(description=info_string, title=f'Information about {server}', color=0xd252e3)
        embed.set_image(url=str(icon_url))
        await ctx.send(embed=embed)

    @commands.command()
    async def new_role(self, ctx, name, r=0, g=0, b=0, level_of_permissions=0, reason=''):
        """
        Create new role
        :param level_of_permissions: You can calculate level of permissions on discord developer portal
        """
        await ctx.guild.create_role(name=name,
                                    color=discord.Color.from_rgb(r=int(r), g=int(g), b=int(b)),
                                    permissions=discord.Permissions(permissions=int(level_of_permissions)),
                                    reason=reason)


def setup(bot):
    bot.add_cog(Guild(bot))
