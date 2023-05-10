import lightbulb

# ----------    BOT OBJECTS    ---------- #
plugin = lightbulb.Plugin("cat_facts")  # Create plugin

# ----------    BOT COMMANDS    ---------- #


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)