import requests
from twitch.message_handler import commands
from commands.record import find_rikishi_id

@commands.add(name="shansho", aliases=[], cooldown=3)
def shanshos(ctx):
    if not ctx.args:
        ctx.reply(f"@{ctx.display_name} Usage: !shanshos <rikishi name>")
        return
    name_query = " ".join(ctx.args).lower()
    result = find_rikishi_id(name_query)
    if not result:
        ctx.reply(f"@{ctx.display_name} No rikishi found for '{name_query}'.")
        return
    rikishi_id, shikona = result
    try:
        stats = requests.get(f"https://www.sumo-api.com/api/rikishi/{rikishi_id}/stats").json()
        sansho = stats.get("sansho", {})
        info = (
            f"{shikona} | Gino-sho: {sansho.get('Gino-sho', 0)} | "
            f"Kanto-sho: {sansho.get('Kanto-sho', 0)} | "
            f"Shukun-sho: {sansho.get('Shukun-sho', 0)}"
        )
        ctx.reply(f"@{ctx.display_name} -> {info}")
    except Exception:
        ctx.reply(f"@{ctx.display_name} -> Error fetching sansho data.")
