import os
import logging
import random

import discord
from discord.ext import commands
import utils


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


# @bot.event
# async def on_message():
#     """runs whenever there's a message the bots can see. I believe"""
#     # logging.info(f'{ctx.author} : {ctx.content}')


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
        rolls, limit = map(int, dice.split("d"))
    except Exception:
        await ctx.send("Format has to be in NdN!")
        return

    result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description="Harness the power of AI to generate a shitpost.")
async def shitpost(ctx, *args):
    """posts a shitpost, can add your own prompt with !shitpost <text>"""
    shitpost_prompt = ""
    if args:
        shitpost_prompt = " ".join(args)
    shitpost_text = await utils.generate_shitpost(shitpost_prompt)
    return await ctx.send(f"This is a shitpost: \n {shitpost_prompt} {shitpost_text}")


@bot.command(description="For choosing between arbitrary choices")
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command(description="For ordering elements randomly")
async def shuffle(ctx, *choices: str):
    """randomize the order of a list of multiple elements."""
    return_list: list[str] = list(choices)
    random.shuffle(return_list)
    await ctx.send("\n".join(return_list))


@shuffle.error
async def info_error(ctx, error):
    if isinstance(error, commands.ExpectedClosingQuoteError):
        await ctx.send(
            "Oops, looks like you forgot to close a quote for one of your arguments"
        )

    if isinstance(error, commands.BadArgument):
        await ctx.send(
            "Oops! There was an error in the way that command was parsed. Please try again"
        )


@bot.command(
    description="Brownies appreciate pets, as long as it doens't interfere with their work"
)
async def pet(ctx):
    """Pet a brownie"""
    await ctx.send("*The little brownie looks at you and smiles as you pet it.*")


bot.run(os.environ["DISCORD_TOKEN"])
