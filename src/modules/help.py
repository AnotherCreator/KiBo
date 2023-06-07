import hikari
import lightbulb

plugin = lightbulb.Plugin("help")


# ----------    BOT COMMANDS    ---------- #
@plugin.command
@lightbulb.command("help", "Command information")
@lightbulb.implements(lightbulb.SlashCommand)
async def help_command(ctx: lightbulb.Context) -> None:
    embed = (
        hikari.Embed(
            title=f"Hi"
        )
        .set_author(
            name=f"Hi"
        )
        .add_field(
            "Daily % Change",
            f"Among",
            inline=False
        )
    )

    await ctx.respond(embed)


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
