import hikari
import lightbulb
import logging
from PyDictionary import PyDictionary

dictionary = PyDictionary()
logger = logging.getLogger()

# ----------    BOT OBJECTS    ---------- #
plugin = lightbulb.Plugin("dictionary")  # Create plugin


# ----------    BOT COMMANDS    ---------- #
@plugin.command
@lightbulb.command("dictionary", "Use the dictionary")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def book(ctx: lightbulb.Context) -> None:
    pass


@book.child
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
    user_translate = ctx.options.translate
    user_antonym = ctx.options.antonym
    user_synonym = ctx.options.synonym
    user_definition = ctx.options.define

    if user_definition is not None:
        logger.info(f"User definition: {dictionary.meaning(user_definition)}")

    if user_synonym is not None:
        logger.info(f"User synonym: {dictionary.synonym(user_synonym)}")

    if user_antonym is not None:
        logger.info(f"User antonym: {dictionary.antonym(user_antonym)}")

    if user_translate is not None:
        logger.info(f"User translation: {dictionary.translate(user_translate, 'tl')}")

    embed = (
        hikari.Embed(title="Hi").add_field("Hi", "Hi", inline=False).add_field("2nd Hi", "2nd Hi", inline=False)
    )
    await ctx.respond(embed)


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
