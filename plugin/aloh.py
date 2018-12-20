import asyncio
import psycopg2
import random
import discord
import re
from discord.ext import commands


class alohclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def 알로세이드(self, ctx, num: int):
        await self.bot.send_message(ctx.message.channel, "알로세이드는 1172번까지 있습니다.")
        if 0 <= num <= 1172:
            await self.alohsaydCore(ctx, num)


    @commands.command(pass_context=True)
    async def 알로세이드랜덤(self, ctx):
        num = random.randrange(0, 1173)
        await self.bot.send_message(ctx.message.channel, "랜덤 알로세이드")
        await self.alohsaydCore(ctx, num)


    async def alohsaydCore(self, ctx, num: int):
        conn = psycopg2.connect(database=database, user=user,
                                password=password, host=host, port=port)
        with conn:
            try:
                cur = conn.cursor()
                cur.execute("select * from alohsayd where num={0}".format(num))
                rows = cur.fetchall()
                row = rows[0]
                print(row)
                num = row[0]
                head = row[1]
                body = row[2]
                head = head.replace("\n", "")
                embed = discord.Embed(
                    title="%s" % head, description="\n%s" % (body), color=0xE0FFFF)
                await self.bot.send_message(ctx.message.channel, embed=embed)
            except:
                await self.bot.send_message(ctx.message.channel, "파일을 찾지 못했어요!")
                pass

def setup(bot):
    bot.add_cog(alohclass(bot))
