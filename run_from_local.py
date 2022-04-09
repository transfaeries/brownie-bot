# all the imports

import glob
import logging
import os
import pickle
import random
import re
import shutil
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, Dataset, RandomSampler, SequentialSampler
from torch.utils.data.distributed import DistributedSampler
from tqdm.notebook import tqdm, trange

from pathlib import Path

from transformers import (
    MODEL_WITH_LM_HEAD_MAPPING,
    WEIGHTS_NAME,
    AdamW,
    AutoConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
    get_linear_schedule_with_warmup,
)


try:
    from torch.utils.tensorboard import SummaryWriter
except ImportError:
    from tensorboardX import SummaryWriter


from transformers import AutoModelForCausalLM, AutoModelForCausalLM, AutoTokenizer
import torch

import random
import time


# the Discord Python API
import discord


class MyClient(discord.Client):
    def __init__(self, model_directory):
        print(os.getcwd())
        self.tokenizer = AutoTokenizer.from_pretrained(model_directory)
        self.model = AutoModelForCausalLM.from_pretrained(model_directory)
        super().__init__()

    def generate_reply(self, input_message):
        new_user_input_ids = self.tokenizer.encode(
            input_message + self.tokenizer.eos_token, return_tensors="pt"
        )

        bot_input_ids = new_user_input_ids

        chat_history_ids = self.model.generate(
            bot_input_ids,
            max_length=200,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8,
        )

        bot_reply = self.tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1] :][0], skip_special_tokens=True
        )
        print("Bot: {}".format(bot_reply))
        return bot_reply

    async def on_ready(self):
        # print out information when the bot wakes up
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

    async def on_message(self, message):
        """
        this function is called whenever the bot sees a message in a channel
        """

        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return

        print(f"{message.author.name} : {message.content}")

        if message.content == "ping":
            bot_response = "pong"
            await message.channel.send(bot_response)
            return

        # while the bot is waiting on a response from the model
        # set the its status as typing for user-friendliness
        async with message.channel.typing():
            response = self.generate_reply(message.content)
        bot_response = response

        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            if "error" in response:
                error_message = "`Error: {}`".format(response["error"])
                if "timed out" in response:
                    bot_response = "hold on nelly, I'm confused"
                elif "is currently loading" in response:
                    bot_response = (
                        "I'm sleepy, give me {} seconds to wake up... zZZZ".format(
                            response["estimated_time"]
                        )
                    )
                else:
                    bot_response = error_message

                print(error_message)
                print(response)
            else:
                bot_response = "Hmm... something is not right."

        # send the model's response to the Discord channel
        await message.channel.send(bot_response)


def main():
    # use model directory
    client = MyClient("../twilight-sparkle-medium-13/output-medium/")
    client.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
