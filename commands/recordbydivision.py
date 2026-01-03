import requests
from twitch.message_handler import commands
from commands.record import find_rikishi_id

@commands.add(name="recordbydivision", aliases=[], cooldown=3)
def recordbydivision(ctx):
    if not ctx.args:
        ctx.reply(f"@{ctx.display_name} Usage: !recordbydivision <rikishi name>")
        return
    name_query = " ".join(ctx.args).lower()
    result = find_rikishi_id(name_query)
    if not result:
        ctx.reply(f"@{ctx.display_name} -> No rikishi found for '{name_query}'.")
        return
    rikishi_id, shikona = result
    try:
        stats = requests.get(f"https://www.sumo-api.com/api/rikishi/{rikishi_id}/stats").json()
        wins = stats.get("winsByDivision", {})
        losses = stats.get("lossByDivision", {})
        divisions = set(wins.keys()) | set(losses.keys())
        records = []
        for div in divisions:
            w = wins.get(div, 0)
            l = losses.get(div, 0)
            records.append(f"{div}: {w}-{l}")
        info = f"{shikona} | " + " | ".join(records)
        ctx.reply(f"@{ctx.display_name} -> {info}")
    except Exception:
        ctx.reply(f"@{ctx.display_name} -> Error fetching division record data.")
