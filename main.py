from camoufox.async_api import AsyncCamoufox
from dotenv import load_dotenv
import discord
import os

load_dotenv()

client = discord.Client()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
INVITE_URL = os.getenv("INVITE_URL")
GUILD_NAME = os.getenv("GUILD_NAME")
SPAM_MESSAGE = os.getenv("SPAM_MESSAGE")

async def OpenCaptcha():
    async with AsyncCamoufox(locale="en-US", fingerprint_preset=True, geoip=True, humanize=False) as browser:
        page = await browser.new_page()
        await page.goto(INVITE_URL)
        await page.evaluate(f'window.localStorage.setItem("token", JSON.stringify("{DISCORD_TOKEN}"))')
        await page.reload()
        await page.click('button[data-mana-component="button"][role="button"][class*="button_"]:has-text("accept invite")')
        await page.frame_locator('iframe[src*="https://newassets.hcaptcha.com/captcha/v1/"][title="Widget containing checkbox for hCaptcha security challenge"]').get_by_role("checkbox").click()
        try:
            await page.wait_for_url("https://discord.com/channels/*")
        except Exception as err:
            print("Captcha not passed or your ip is temporarily blocked!")

async def EnterSpamLeave():
    await client.accept_invite(INVITE_URL)
    print("Successfully join to guild!")
    for guild in client.guilds:
        if (guild.name == GUILD_NAME):
            for ch in client.get_guild(guild.id).text_channels:
                try:
                    await ch.send(SPAM_MESSAGE)
                except discord.errors.Forbidden:
                    print(f"Channel '{ch.name}({ch.id})' is closed, no access!")
            await guild.leave()  
            print("Successfully leave from guild!")  

@client.event
async def on_ready():
    while True:
        try:
            await EnterSpamLeave()
        except discord.CaptchaRequired as err:
            print("Oh no... Captcha!")
            await OpenCaptcha()
            await EnterSpamLeave()

client.run(DISCORD_TOKEN)