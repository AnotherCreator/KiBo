import hikari
import json
import lightbulb
import logging
import os
import psycopg2 as psycopg2
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

logger = logging.getLogger()

# ----------    BOT OBJECTS    ---------- #
plugin = lightbulb.Plugin("market")  # Create plugin

# ----------    ENV VARS  ---------- #
CMC_API_KEY = os.environ.get("CMC_API_KEY")
DATABASE_PW = os.environ.get("DATABASE_PW")
BOT_AVATAR = os.environ.get("BOT_AVATAR")

# ----------    LOAD API   ---------- #
api_data = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
api_metadata = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"

headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": CMC_API_KEY,
}

session = Session()
session.headers.update(headers)

# ----------    API PARAMETERS   ---------- #
coin_parameters = {  # Retrieve coins listed 1-100
    "start": "1",
    "limit": "100",
    "convert": "USD",
    "aux": "cmc_rank"
}

# ----------    CONNECT TO DB   ---------- #
con = psycopg2.connect(
    host="localhost",
    database="pybo_official",
    user="postgres",
    password=DATABASE_PW
)
cur = con.cursor()

# ----------    DATABASE FUNCTIONS  ---------- #
"""
def cache_coins():

This function is only used once and will instantiate all the coins within the PostgreSQL database
This should not be run during bot start in bot.py
Once the coin data has be initialized in the database, you can remove the function call and update_coins() will take over
"""


def cache_coins():
    try:
        id_list = []
        coin_response = session.get(api_data, params=coin_parameters)
        coin_data = json.loads(coin_response.text)
        coins = coin_data["data"]

        for x in coins:
            id_list.append(x["id"])
            ids = x["id"]
            rank = x["cmc_rank"]
            name = x["name"]
            symbol = x["symbol"]
            price = x["quote"]["USD"]["price"]
            daily_change = x["quote"]["USD"]["percent_change_24h"]

            cur.execute("INSERT INTO coin_info"
                        "(coin_id, coin_name, coin_symbol, coin_price, coin_rank, coin_daily_change)"
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (ids, name, symbol, price, rank, daily_change))
            con.commit()  # Commit transaction

        joined_id = ",".join(map(str, id_list))  # Creates comma-separated string

        metadata_parameters = {  # Retrieves coin_metadata listed 1-100
            "id": joined_id,
            "aux": "logo"
        }
        metadata_response = session.get(api_metadata, params=metadata_parameters)
        metadata_data = json.loads(metadata_response.text)
        metadata = metadata_data["data"]

        for unique_id in id_list:
            logo_url = metadata[str(unique_id)]["logo"]

            cur.execute("UPDATE coin_info "  # Uses UPDATE instead of INSERT since first insertion init coin_logo column
                        "SET coin_logo = %s "
                        "WHERE coin_id = %s ",
                        (logo_url, unique_id))
            con.commit()  # Commit transaction
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


"""
def update_coins():

This function will just update all the coin values inside the database on a set interval defined within bot.py 
refresh_coins() function
"""


def update_coins():
    try:
        coin_response = session.get(api_data, params=coin_parameters)
        coin_data = json.loads(coin_response.text)
        coins = coin_data["data"]

        for x in coins:
            coin_id = x["id"]
            rank = x["cmc_rank"]
            price = x["quote"]["USD"]["price"]
            daily_change = x["quote"]["USD"]["percent_change_24h"]

            cur.execute("UPDATE coin_info "
                        "SET coin_price = %s, coin_rank = %s, coin_daily_change = %s "
                        "WHERE coin_id = %s",
                        (price, rank, daily_change, coin_id))
            con.commit()  # Commit transaction
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


# ----------    HELPER FUNCTIONS  ---------- #
def db_entry_found(x: tuple) -> logger:
    logger.info(f"Database entry found: {x[0], x[1], x[2], x[3], x[4], x[5]}")
    pass


def create_single_coin_embed(x: tuple) -> hikari.Embed():
    embed = (
        hikari.Embed(
            title=f"${str(x[3])}"
        )
        .set_author(
            name=f"{x[4]}. {x[1]} / {x[2]}",
            icon=x[6]
        )
        .add_field(
            "Daily % Change",
            f"{x[5]:.2f}%",
            inline=False
        )
    )

    return embed


# ----------    BOT COMMANDS    ---------- #
@plugin.command
@lightbulb.command("market", "Display coin info")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def coins(ctx: lightbulb.Context) -> None:
    pass


@coins.child()  # Fetch coin info via coin ranking #
@lightbulb.option("number", "Displays current coin info for the ranked coin",
                  type=int, required=False, min_value=0, max_value=100, default=None)
@lightbulb.option("name", "Displays current coin info for the ranked coin",
                  type=str, required=False, default=None)
@lightbulb.command("rank", "Enter a coin rank")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def coin_rank(ctx: lightbulb.Context) -> None:
    # Database
    cur.execute("SELECT * FROM coin_info ORDER BY coin_rank asc")
    rows = cur.fetchall()

    # Assign option values to variables
    coin_number = ctx.options.number
    coin_name = ctx.options.name

    embed = hikari.Embed()
    if coin_number is not None:
        logger.info(f"User entered a coin rank: {coin_number}")

        for x in rows:
            # ID: x[0] || Name: x[1] || Symbol: x[2] || Price: x[3] || Rank: x[4] || Change: x[5] || Logo: x[6]
            if x[4] == coin_number:
                db_entry_found(x)  # Logger function
                embed = create_single_coin_embed(x)

    if coin_name is not None:
        logger.info(f"User entered a coin name: {coin_name}")

        for x in rows:
            # ID: x[0] || Name: x[1] || Symbol: x[2] || Price: x[3] || Rank: x[4] || Change: x[5] || Logo: x[6]
            if x[1].lower() == coin_name.lower():
                db_entry_found(x)  # Logger function
                embed = create_single_coin_embed(x)
    await ctx.respond(embed)


@coins.child()  # Fetch top 10 coins respective to user input (50 ==> 40...50)
@lightbulb.option("top", "Displays the top 10 coins of the respective rank",
                  type=int, required=False, default=10)
@lightbulb.command("list", "Enter a coin rank")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def coin_list(ctx: lightbulb.Context) -> None:
    # Database
    cur.execute('SELECT * FROM coin_info ORDER BY coin_rank asc')  # 1,2,3...,100
    rows = cur.fetchall()

    # Assign option values to variables
    rank = ctx.options.top

    if rank < 11:
        current_min = 1
        current_max = 10
    else:
        current_min = rank - 10
        current_max = rank
        if current_max > 100:
            current_max = 100

    embed = hikari.Embed(
        title=' ',
        description=' ',
        color="#5865F2"
    )
    #  ID: x[0] || Name: x[1] || Symbol: x[2] || Price: x[3] || Rank: x[4] || Change: x[5] || Logo: x[6]
    for x in rows:
        if current_min <= x[4] <= current_max:
            embed.set_author(name=f'Top {current_max} Crypto Coins', icon=BOT_AVATAR)
            embed.add_field(
                name=f'{x[4]}. {x[1]} / {x[2]}',
                value=f'${x[3]}',
                inline=False)
            embed.set_footer(text="")

    await ctx.respond(embed)


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
