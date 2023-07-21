# daily.py
import hikari
import lightbulb
from apscheduler.triggers.cron import CronTrigger


plugin = lightbulb.Plugin("Daily")


async def msg1() -> None:
    await plugin.app.rest.create_message(1131601875251245157, "Is Kami Back?\nNo, he will be back <t:1691096400:R> on"
                                                              " <t:1691096400:F>")


@plugin.listener(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    # This event fires once, when the BotApp is fully started.
    plugin.app.d.sched.add_job(msg1, CronTrigger(hour="*/12", end_date='2023-08-03'))


# ----------    LOAD PLUG-IN   ---------- #
def load(bot):
    bot.add_plugin(plugin)
