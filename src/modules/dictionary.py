import hikari
import lightbulb
import logging
from PyDictionary import PyDictionary

dictionary = PyDictionary()
logger = logging.getLogger()

# ----------    BOT OBJECTS    ---------- #
plugin = lightbulb.Plugin("dictionary")  # Create plugin


# ----------    HELPER FUNCTIONS    ---------- #
def create_dictionary_embed(user_input, dictionary_results) -> hikari.Embed():
    embed = (
        hikari.Embed(
            title=f"{user_input}"
        )
    )

    for key, value in dictionary_results.items():
        embed.add_field(
            key,
            value,
            inline=False
        )

    return embed

# ----------    BOT COMMANDS    ---------- #
@plugin.command
@lightbulb.command("book", "A list of books")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def book(ctx: lightbulb.Context) -> None:
    pass


@book.child()
@lightbulb.option("translate", "Translate a word into another language",
                  required=False, type=str, default=None, min_length=1)
@lightbulb.option("antonym", "Find the antonym of a word",
                  required=False, type=str, default=None, min_length=1)
@lightbulb.option("synonym", "Find the synonym of a word",
                  required=False, type=str, default=None, min_length=1)
@lightbulb.option("define", "Find the definition of a word",
                  required=False, type=str, default=None, min_length=1)
@lightbulb.command("dictionary", "Use the dictionary")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def use_dictionary(ctx: lightbulb.Context) -> None:
    # Get user input
    user_antonym = ctx.options.antonym
    user_synonym = ctx.options.synonym
    user_definition = ctx.options.define

    embed = hikari.Embed()  # Instantiate embed obj

    if user_definition is not None:
        logger.info(f"User definition: {user_definition}:{dictionary.meaning(user_definition)}")
        embed = create_dictionary_embed(user_definition, dictionary.meaning(user_definition))

    # if user_synonym is not None:
    #     logger.info(f"User synonym: {user_synonym}:{dictionary.synonym(user_synonym)}")
    #     embed = create_dictionary_embed(user_synonym, dictionary.synonym(user_synonym))
    #
    # if user_antonym is not None:
    #     logger.info(f"User antonym: {user_antonym}:{dictionary.antonym(user_antonym)}")
    #     embed = create_dictionary_embed(user_antonym, dictionary.antonym(user_antonym))

    await ctx.respond(embed)


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
