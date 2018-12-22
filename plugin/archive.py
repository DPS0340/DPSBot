import os
import sys
import archiveis
import asyncio
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from plugin.whisperandlog import bot_log

class archiveclass():
    def __init__(self, bot):
        self.bot = bot
        proxyString = "13.209.8.211:80"
        desired_capability = webdriver.DesiredCapabilities.FIREFOX
        desired_capability['proxy'] = {
            "proxyType": "manual",
            "httpProxy": proxyString,
            "sslProxy": proxyString
        }
        desired_capability["unexpectedAlertBehaviour"] = "accept"
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        options.add_argument('--mute-audio')
        try:
            profile = webdriver.FirefoxProfile()
            profile.set_preference("media.volume_scale", "0.0")
            profile.set_preference("intl.accept_languages", "ko")
            driver = webdriver.Firefox(profile, firefox_options=options)
            options.add_argument(
                {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'})
        except:
            pass


    @commands.command(pass_context=True)
    async def 아카이브(self, ctx, url):
        await bot_log("%s가 %s를(을) 아카이브 했습니다.\n" % (ctx.message.author, url))
        try:
            if not "http" in url:
                url = "http://" + url
            archive_url = archiveis.capture(url, proxyString)
            await bot.send_message(ctx.message.channel, "아카이브 중입니다...\n"
                                                        "조금만 기다려 주세요!")
            driver.get(url)
            wait = WebdriverWait(driver, 2)
            wait.until(EC.presence_of_element_located((By.XPATH, 'html')))
            driver.maximize_window()
            driver.find_element_by_tag_name('html').screenshot('screenshot.png')
            await bot.send_file(ctx.message.channel, 'screenshot.png')
            await bot.send_message(ctx.message.channel, archive_url)
            await bot_log("아카이브 주소:%s\n" % (url))
        except:
            try:
                driver.close()
            except:
                pass
            await self.bot.send_message(ctx.message.channel, "오류가 발생했어요!")
            raise


def setup(bot):
    bot.add_cog(archiveclass(bot))