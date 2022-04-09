import discord
import os
import time
import logging
import asyncio



import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


class MyClient(discord.Client):
    async def on_ready(self):
        self.last_message: str = ""
        print('Logged on as', self.user)
        logging.getLogger().setLevel("INFO")
        logging.info('Logged on as %s',self.user)

    async def on_message(self, message: discord.message):
        """How the bot reacts to being messaged"""
        logging.info("%s : %s", message.author,message.content)
        asyncio.sleep(1)
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == self.last_message:
            return

        self.last_message = message.content

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content == '!post':
            await self.post_a_shitpost(message)

    async def post_a_shitpost(self,message):
        await message.channel.send("This is a shitpost")







client = MyClient()
client.run(os.environ['DISCORD_TOKEN'])