import psycopg2
from variables import DATABASE_URL, owner, mod
import asyncio
from discord.ext import commands

class modclass():
    def __init__(self, bot):
        self.bot = bot
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute('select * from mod')
        rows = cur.fetchall()
        print('부운영자 로드중...')
        print('------')
        for row in rows:
            try:
                id = row[0]
                mod.append(str(id))
                name = await self.bot.get_user_info(id)
                print(name)
            except:
                print('부운영자 로드 실패!')
                pass
        conn.close()
        print('------')
        print('부운영자 로드 완료!')

    @commands.command(pass_context=True)
    async def 부운영자추가(self, ctx):
        if ctx.message.author.id == owner or ctx.message.author.id in mod:
            userid = ctx.message.mentions[0].id
            mod.append(userid)
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute("""insert into mod ("id") values (%s)""" % userid)
            conn.commit()
            conn.close()
            person = await self.bot.get_user_info(userid)
            await self.bot.send_message(ctx.message.channel, "%s 부운영자 등록 완료!" % person.name)
        else:
            await self.bot.send_message(ctx.message.channel, "당신은 권한이 없습니다.\n당신이 봇의 운영자거나 부운영자인지 확인해 보세요.")

    @commands.command(pass_context=True)
    async def 부운영자삭제(self, ctx):
        if ctx.message.author.id == owner or ctx.message.author.id in mod:
            userid = ctx.message.mentions[0].id
            mod.remove(userid)
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute("""delete from mod where id = '%s'""" % userid)
            conn.commit()
            conn.close()
            person = await self.bot.get_user_info(userid)
            await self.bot.send_message(ctx.message.channel, "%s 부운영자 삭제 완료!" % person.name)
        else:
            await self.bot.send_message(ctx.message.channel, "당신은 권한이 없습니다.\n당신이 봇의 운영자거나 부운영자인지 확인해 보세요.")

    @commands.command(pass_context=True)
    async def 부운영자확인(self, ctx):
        messagebody = "부운영자 목록\n"
        for userid in mod:
            person = await self.bot.get_user_info(userid)
            messagebody += person.name + " "
        await self.bot.send_message(ctx.message.channel, messagebody)

    

def setup(bot):
    bot.add_cog(modclass(bot))
