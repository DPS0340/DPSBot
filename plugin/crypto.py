import asyncio
from discord.ext import commands
from cryptography.fernet import Fernet


class cryptoclass():
    def __init__(self, bot):
        self.bot = bot
        privatekey = Fernet.generate_key()
        self.cipher_suite = Fernet(privatekey)

    @commands.command(pass_context=True)
    async def 암호화(self, ctx):
        await self.bot.say('암호화시킬 내용을 말해주세요.')
        plaintext = await self.bot.wait_for_message(author=ctx.message.author)
        if plaintext:
            encryptedtext = self.cipher_suite.encrypt(plaintext.content.encode("utf-8")).decode()
            await self.bot.say(encryptedtext)
        else:
            await self.bot.say('내용이 없습니다.')

    @commands.command(pass_context=True)
    async def 복호화(self, ctx):
        await self.bot.say('암호를 말해주세요.')
        encryptedtext = await self.bot.wait_for_message(author=ctx.message.author)
        if encryptedtext:
            plaintext = self.cipher_suite.decrypt(encryptedtext.content.encode("utf-8")).decode()
            await self.bot.say(plaintext)
        else:
            await self.bot.say('내용이 없습니다.')


def setup(bot):
    bot.add_cog(cryptoclass(bot))