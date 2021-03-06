from discord.ext import commands
import asyncio
import discord
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from pluginlist import pluginlist
from embed import Embed


class pluginclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="module", aliases=["모듈"], pass_context=True)
    async def module(self, ctx):
        i = 0
        body = ""
        for plugin in pluginlist.get()["default"]:
            i += 1
            body += plugin + " "
            if i % 5 == 0:
                body += '\n'
        embed = Embed(title=_("사용중인 모듈 리스트"),
                      description=body, color=0x00FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)
        i = 0
        body = ""
        for plugin in pluginlist.get()["non-default"]:
            i += 1
            body += plugin + " "
            if i % 5 == 0:
                body += '\n'
        embed = Embed(title=_("사용 가능한 모듈 리스트"),
                      description=body, color=0xE0FFFF)
        await self.bot.send_message(ctx.message.channel, embed=embed)
        await self.bot.say("sorry! module setting for each channel is not yet.")


def setup(bot):
    bot.add_cog(pluginclass(bot))
