import os
import logging
import random

import discord
from discord.ext import commands


logging.basicConfig(level=logging.INFO)


DESCRIPTION = """Helpful bot that helps take care of the embassy"""

intents = discord.Intents.default()
intents.members = True
# intents.message_content = True

bot = commands.Bot(command_prefix="!", description=DESCRIPTION, intents=intents)


@bot.event
async def on_ready():
    """runs when bot is ready"""
    logging.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    logging.info("------")


@bot.command()
async def ping(ctx, *args):
    """Ping the bot. !ping <text> will return the text also"""
    if args:
        return await ctx.send("pong " + " ".join(args))
    return await ctx.send("pong")

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def post(ctx):
    """posts a shitpost"""
    return await ctx.send("this is a shitpost")


@bot.command(description='For choosing between arbitrary choices')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))
    



bot.run(os.environ["DISCORD_TOKEN"])
