import os
import logging
import pluralkit
import openai
import discord

pk = pluralkit.Client(os.getenv('PK_TOKEN',""))
openai.api_key = os.getenv("GOOSEAI_API_KEY","")
openai.api_base = "https://api.goose.ai/v1"
# log_level=os.environ.get('LOG_LEVEL' ,"INFO")
logging.basicConfig(level=logging.INFO)

async def pk_switch():

    time,front = await pk.get_fronters()
    if front is None:
        front = "no one"
    logging.info(f"{time}: {front} is in front to start with")

    members = pk.get_members()
    async for member in members:
        logging.info(f"{member.name} (`{member.id}`)")

async def generate(prompt : str = "") -> str:
        response = openai.Completion.create(  # type: ignore
            engine="gpt-neo-1-3b",
            prompt=prompt,
            temperature=0.9,
            max_tokens=140,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop = ["\n\n"]
        )
        return response["choices"][0]["text"].strip()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())