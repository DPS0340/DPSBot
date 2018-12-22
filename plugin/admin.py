from discord.ext import commands
import asyncio
from variables import owner, pluginfolder, instructions, gamename, prefix
from pluginlist import lst as pluginlist
import psycopg2
import os
import discord
import sys
from embed import Embed
DATABASE_URL = os.environ['DATABASE_URL']
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class adminclass():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, pass_context=True)
    async def load(self, ctx, *modules):
        if ctx.message.author.id == owner:
            for module in modules:
                try:
                    if not module in pluginlist:
                        pluginlist.append(module)
                        self.bot.load_extension(pluginfolder + module)
                        await self.bot.say('%s 모듈 로드 완료!' % module)
                    else:
                        await self.bot.say('이미 로드된 모듈입니다.')
                except Exception as e:
                    await self.bot.say('오류 발생!\n%s' % e)
        else:
            await self.bot.say('권한이 없습니다.\n운영자만 사용 가능합니다.')

    @commands.command(hidden=True, pass_context=True)
    async def unload(self, ctx, *modules):
        if ctx.message.author.id == owner:
            for module in modules:
                if module == "admin":
                    await self.bot.say('어드민 모듈은 모듈을 로드하고 해제하는 기능이 있어, 해제가 불가능합니다.')
                else:
                    try:
                        if module in pluginlist:
                            pluginlist.remove(module)
                            self.bot.load_extension(pluginfolder + module)
                            await self.bot.say('%s 모듈 해제 완료!' % module)
                        else:
                            await self.bot.say('이미 해제된 모듈입니다.')
                    except Exception as e:
                        await self.bot.say('오류 발생!\n%s' % e)
        else:
            await self.bot.say('권한이 없습니다.\n운영자만 사용 가능합니다.')

    @commands.command(hidden=True, pass_context=True)
    async def reload(self, ctx, *modules):
        if ctx.message.author.id == owner:
            for module in modules:
                if module == "admin":
                    await self.bot.say('어드민 모듈은 모듈을 로드하고 해제하는 기능이 있어, 재로드가 불가능합니다.')
                else:
                    try:
                        self.bot.unload_extension(pluginfolder + module)
                        self.bot.load_extension(pluginfolder + module)
                        if not module in pluginlist:
                            pluginlist.append(module)
                        await self.bot.say('%s 모듈 재로드 완료!' % module)
                    except Exception as e:
                        await self.bot.say('오류 발생!\n%s' % e)
        else:
            await self.bot.say('권한이 없습니다.\n운영자만 사용 가능합니다.')


    @commands.command(hidden=True, pass_context=True)
    async def 봇소개변경(self, ctx):
        if ctx.message.author.id == owner:
            await self.bot.say("변경할 내용을 말해주세요.")
            msg = await self.bot.wait_for_message(author=ctx.message.author)
            if msg:
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                conn.autocommit = True
                cur = conn.cursor()
                cur.execute("update settings set body = '%s' where name='instructions'" % msg.content)
                conn.close()
                instructions.set(msg.content)
                await self.bot.say("변경 완료.")
        else:
            await self.bot.say('권한이 없습니다.\n운영자만 사용 가능합니다.')


    @commands.command(hidden=True, pass_context=True)
    async def 플레이중추가(self, ctx):
        if ctx.message.author.id == owner:
            await self.bot.say("변경할 내용을 말해주세요.")
            msg = await self.bot.wait_for_message(author=ctx.message.author)
            if msg:
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                conn.autocommit = True
                cur = conn.cursor()
                cur.execute("update settings set body = '%s' where name='game'" % msg.content)
                conn.close()
                gamename.append(msg.content)
                await self.bot.change_presence(game=discord.Game(name=gamename.get()))
                await self.bot.say("%s로 변경되었습니다." % msg.content)
        else:
            await self.bot.say('권한이 없습니다.\n운영자만 사용 가능합니다.')


    @commands.command(hidden=True, pass_context=True)
    async def 접두사변경(self, ctx):
        if ctx.message.author.id == owner:
            await self.bot.say("변경할 내용을 말해주세요.\n공백은 _으로 대체하세요.")
            msg = await self.bot.wait_for_message(author=ctx.message.author)
            if msg:
                new_prefix = msg.content
                new_prefix = new_prefix.replace("_", " ")
                conn = psycopg2.connect(DATABASE_URL, sslmode='require')
                conn.autocommit = True
                cur = conn.cursor()
                cur.execute("update settings set body = '%s' where name='prefix'" % new_prefix)
                conn.close()
                prefix.set(new_prefix)
                await self.bot.say("%s로 접두사가 변경되었습니다.\n봇을 재시작시켜주세요." % new_prefix)
        else:
            await self.bot.say('권한이 없습니다.\n운영자만 사용 가능합니다.')


    @commands.command(hidden=True, pass_context=True)
    async def 명령어삭제(self, ctx, *functions):
        if ctx.message.author.id == owner:
            embed = Embed(title="**경고**", description="현재 이 기능은 불안정하므로, 주의해서 사용하시길 바랍니다.", color=0xff0000)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            for function in functions:
                try:
                    self.bot.remove_command(function)
                    await self.bot.say("%s 명령어 삭제 완료." % function)
                except Exception as e:
                    await self.bot.say("오류가 발생했습니다." % function)
                    await self.bot.say(e)
        else:
            await self.bot.say('권한이 없습니다.\n운영자만 사용 가능합니다.')


    @commands.command(hidden=True, pass_context=True)
    async def 명령어복구(self, ctx, *functions):
        if ctx.message.author.id == owner:
            embed = Embed(title="**경고**", description="현재 이 기능은 불안정하므로, 주의해서 사용하시길 바랍니다.", color=0xff0000)
            await self.bot.send_message(ctx.message.channel, embed=embed)
            for function in functions:
                try:
                    self.bot.add_command(function)
                    await self.bot.say("%s 명령어 복구 완료." % function)
                except Exception as e:
                    await self.bot.say("오류가 발생했습니다." % function)
                    await self.bot.say(e)
        else:
            await self.bot.say('권한이 없습니다.\n운영자만 사용 가능합니다.')


def setup(bot):
    bot.add_cog(adminclass(bot))