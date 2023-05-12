import hikari
import lightbulb
import os
from dotenvy import load_env, read_file
from lightbulb.ext import tasks

# ---------- LOAD ENV VARIABLES ---------- #
load_env(read_file('.env'))
BOT_SECRET = os.environ.get("BOT_SECRET")
DEV_SERVER_ID = os.environ.get("DEV_SERVER_ID")

# ---------- BOT INITIALIZATION ---------- #
bot = lightbulb.BotApp(
    token=BOT_SECRET,
    intents=hikari.Intents.ALL
)
tasks.load(bot)

# ----------  LOAD EXTENSIONS   ---------- #
# bot.load_extensions("modules.cat_facts")
# bot.load_extensions("modules.help")
bot.load_extensions("modules.market")
bot.load_extensions("modules.dictionary")

# Extensions must be loaded before importing from those specific modules
from src.modules.market import update_coins

# ----------     MAIN LINE      ---------- #
if __name__ == '__main__':
    # ----------    BACKGROUND TASKS    ---------- #
    # Update coin database to reflect 5-min changes
    @tasks.task(s=300)
    async def refresh_coins():
        update_coins()
        print("Coins successfully updated")

    # ----------    RUN BOT & TASKS    ---------- #
    # refresh_coins.start()  # Comment out when testing new modules to prevent API usage
    bot.run(
        activity=hikari.Activity(
            name=f"iTakeDonations", type=hikari.ActivityType.WATCHING)
    )
