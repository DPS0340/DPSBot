import asyncio
import psycopg2
import discord
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
from variables import DATABASE_URL, owner, mod, prefix
from discord.ext import commands
from embed import Embed


class postclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="write", alias=["써줘"], pass_context=True)
    async def write(self, ctx, *, head=None):
        conn = psycopg2.connect(DATABASE_URL)
        with conn:
            try:
                cur = conn.cursor()
                num = cur.lastlowid
                num += 1
            except:
                num = 1
                pass
        if not head:
            await self.bot.send_message(ctx.message.channel, _("제목이 없습니다."))
        else:
            await self.bot.send_message(ctx.message.channel, _("내용을 말해주세요!"))
            body = await self.bot.wait_for_message(timeout=600, author=ctx.message.author)
            body = body.content
            author = ctx.message.author.name
            embed = Embed(title="%s" % head, description="\nby %s\n%s" % (
                author, body), color=0xE0FFFF)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            await self.postinsert("post", num, author, head, body)
    @commands.command(name="post", aliases=["글"], pass_context=True)
    async def post(self, ctx, select=0):
        if select == 0:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute('select * from post')
            rows = cur.fetchall()
            for row in rows:
                num = row[0]
                author = row[1]
                head = row[2]
                await self.bot.send_message(ctx.message.channel, "%s. %s - by %s\n" % (num, head, author))
            conn.close()
            await self.bot.send_message(ctx.message.channel, _("%s글 (번호)를 입력하시면 글을 보실수 있어요!") % prefix.get())
            await self.bot.send_message(ctx.message.channel, _("글을 쓰시려면 %s써줘 (번호)와 제목을 한 줄에 쓰세요!") % prefix.get())
        else:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute('select * from post where num = {0}'.format(select))
            row = cur.fetchone()
            num = row[0]
            author = row[1]
            head = row[2]
            body = row[3]
            conn.close()
            embed = Embed(title="%s. %s" % (
                num, head), description="\nby %s\n%s" % (author, body), color=0xE0FFFF)
            await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(name="deletepost", aliases=["글삭제"], pass_context=True)
    async def deletepost(self, ctx, select: int):
        if ctx.message.author.id == owner or ctx.message.author.id in mod:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()
            cur.execute("""delete from post where num = %d""" % select)
            conn.commit()
            conn.close()
            await self.bot.send_message(ctx.message.channel, _("%d 글 삭제 완료!") % select)
        else:
            await self.bot.send_message(ctx.message.channel, _("당신은 권한이 없습니다.\n당신이 봇의 소유자거나 관리자인지 확인해 보세요."))

    async def postinsert(self, table, num, author, head, body):
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        sql = cur.mogrify("""insert into {0} ("num","author","head","body") values (%s, %s, %s, %s)""".format(
            table), (int(num), str(author), str(head), str(body)))
        cur.execute(sql)
        conn.commit()
        conn.close()


def setup(bot):
    bot.add_cog(postclass(bot))
