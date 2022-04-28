import tweepy
import pluralkit
import os
import logging
import asyncio

pk = pluralkit.Client(os.environ['PK_TOKEN'])
logging.basicConfig(level=logging.INFO)

class pkHelper:
    def __init__(self) -> None:
        pass

    async def main():

        time,front = await pk.get_fronters()
        if front is None:
            front = "no one"
        logging.info(f"{time}: {front} is in front to start with")

        members = pk.get_members()
        async for member in members:
            logging.info(f"{member.name} (`{member.id}`)")

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())