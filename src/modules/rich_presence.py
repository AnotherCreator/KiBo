import lightbulb

# ----------    BOT OBJECTS    ---------- #
plugin = lightbulb.Plugin("rich_presence")  # Create plugin


# ----------    BOT COMMANDS    ---------- #
@plugin.command
# @lightbulb.option("username", "Enter user to find what they're playing!", type=str)
@lightbulb.command("activity", "get user activity!")
@lightbulb.implements(lightbulb.SlashCommand)
async def act(ctx):
    user_presence = ctx.member.get_presence()  # User who called command

    print(user_presence.activities)  # User who called command - will throw error if user is invisible
    if len(user_presence.activities) == 1:
        user_current_game = user_presence.activities[0].name
    elif len(user_presence.activities) == 2:
        user_current_game = user_presence.activities[1].name

    if user_current_game.find("PyCharm") != -1:
        print(f"User is currently playing {user_current_game}")


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
