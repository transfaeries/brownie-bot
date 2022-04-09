import os
import logging
import discord
from discord.ext import commands


logging.basicConfig(level=logging.INFO)


DESCRIPTION = """Helpful bot that helps take care of the embassy"""

intents = discord.Intents.default()
# intents.members = True
# intents.message_content = True

bot = commands.Bot(command_prefix="!", description=DESCRIPTION, intents=intents)


@bot.event
async def on_ready():
    """runs when bot is ready"""
    logging.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logging.info("------")


@bot.command()
async def ping(ctx, *args):
    """Ping the bot"""
    if args:
        return await ctx.send("pong " + " ".join(args))
    return await ctx.send("pong")


bot.run(os.environ["DISCORD_TOKEN"])
