import hikari
import lightbulb
from PyDictionary import PyDictionary

dictionary = PyDictionary()

# ----------    BOT OBJECTS    ---------- #
plugin = lightbulb.Plugin("dictionary")  # Create plugin


# ----------    BOT COMMANDS    ---------- #
@plugin.command
@lightbulb.command("dictionary", "Use the dictionary!")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def dictionary(ctx):
    pass

@dictionary.child
@lightbulb.option("translate", "Translate a word into another language", required=False)
@lightbulb.option("antonym", "Find the antonym of a word", required=False)
@lightbulb.option("synonym", "Find the synonym of a word", required=False)
@lightbulb.option("define", "Find the definition of a word", required=True)
@lightbulb.command("definition", "Find the definition of a word")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def use_dictionary(ctx):
    embed = (
        hikari.Embed(title="Hi").set_author(name="Hi").add_field("Hi", "Hi")
    )
    await ctx.respond(embed)


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
