import asyncio
import re
from datetime import datetime, timedelta
import os

import discord
from discord.ext import commands

# Message Data from config
message_data = discord.Message
custom_response = ""
is_configured = False
interval = ""


async def send_message(message, response):
    try:
        await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f"{bot.user} is now running!")
        try:
            await bot.tree.sync()
        except Exception as e:
            print(e)
        await schedule_ping()

    @bot.tree.command()
    async def bump(
        interaction: discord.Interaction,
    ):  # /bump to keep the bot and badge active
        await interaction.response.send_message("bumpala", ephemeral=True)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        if "?configure" in user_message:
            param_array = re.findall(r"[^\s']+\b|'[^']*'", str(user_message))
            if len(param_array) < 3:
                await send_message(
                    message,
                    "use: ?configure ['message'] [interval]    \nto set up this channel for notifications"
                    "\nan example would be: ?configure 'hello World!' seconds=10,minutes=5,hours=10,days=1",
                )
                return

            global message_data
            message_data = message
            global is_configured
            is_configured = True
            global custom_response
            custom_response = param_array[1].replace("'", "")
            global interval
            interval = param_array[2]

            await send_message(message, "setup successful")
            print(f"target:{username} channel:{channel}")

        elif "help" in user_message:
            await send_message(
                message,
                "use: ?configure ['message'] [interval]    \nto set up this channel for notifications"
                "\nan example would be: ?configure 'hello World!' seconds=10,minutes=5,hours=10,days=1",
            )

    @bot.event
    async def on_timer_trigger():
        await send_message(
            message_data, f"<@{message_data.author.id}>\n" + custom_response
        )

    async def schedule_ping():
        while True:
            now = datetime.now()
            cvargs = dict(re.findall(r"(\w+)=(\d+)", interval))
            cvargs = {k: int(v) for k, v in cvargs.items()}
            try:
                then = now + timedelta(**cvargs)
            except Exception as e:
                print(e)
                then = now + timedelta(
                    days=29
                )  # default to get notified for the badge
            wait_time = (then - now).total_seconds()

            await asyncio.sleep(wait_time)
            bot.dispatch("timer_trigger")

    if os.environ.get("NOTI_BOT_SECRET"):
        bot.run(
            token=os.environ.get("NOTI_BOT_SECRET"),
        )
    else:
        os.environ["NOTI_BOT_SECRET"] = input(
            "Please provide the secret for you discord application: ",
        )
        bot.run(
            token=os.environ.get("NOTI_BOT_SECRET"),
        )
