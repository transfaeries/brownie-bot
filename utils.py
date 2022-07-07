import os
import logging
import pluralkit
import openai
import discord

pk = pluralkit.Client(os.getenv("PK_TOKEN", ""))
openai.api_key = os.getenv("OPENAI_API_KEY", "")
shitpost_engine = os.getenv("SHITPOST_MODEL", "text-curie-001")

# set up logging
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


async def pk_switch():

    time, front = await pk.get_fronters()
    if front is None:
        front = "no one"
    logging.info(f"{time}: {front} is in front to start with")

    members = pk.get_members()
    async for member in members:
        logging.info(f"{member.name} (`{member.id}`)")


#Prompts Open AI for a tweet
def generate(prompt: str = "", engine = "text-curie-001") -> str:
    response = openai.Completion.create(  # type: ignore
        engine=engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0.99,
        presence_penalty=0.3,
        stop=["\n\n"],
    )
    return response["choices"][0]["text"].strip()


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
