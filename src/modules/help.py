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


@plugin.command
@lightbulb.command("kami", "Is he back?")
@lightbulb.implements(lightbulb.SlashCommand)
async def kami_command(ctx: lightbulb.Context) -> None:
    embed = (
        hikari.Embed(
            title=f"Is Kami Back?"
        )
        .add_field(
            "No",
            "he will be back <t:1691096400:R> on <t:1691096400:F>",
            inline=False
        )
    )

    await ctx.respond(embed)


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
