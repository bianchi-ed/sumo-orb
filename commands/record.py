import requests
from twitch.message_handler import commands

def find_rikishi_id(name_query):
    r = requests.get("https://www.sumo-api.com/api/rikishis")
    r.raise_for_status()
    rikishis = r.json()
    if not isinstance(rikishis, list):
        if isinstance(rikishis, dict) and "records" in rikishis and isinstance(rikishis["records"], list):
            rikishis = rikishis["records"]
        else:
            return None
    for rikishi in rikishis:
        if name_query == rikishi.get("shikonaEn", "").lower():
            return rikishi["id"], rikishi.get("shikonaEn", name_query)
    return None

@commands.add(name="record", aliases=[], cooldown=3)
def record(ctx):
    if not ctx.args:
        ctx.reply(f"@{ctx.display_name} Usage: !record <rikishi name>")
        return
    name_query = " ".join(ctx.args).lower()
    result = find_rikishi_id(name_query)
    if not result:
        ctx.reply(f"@{ctx.display_name} No rikishi found for '{name_query}'.")
        return
    rikishi_id, shikona = result
    try:
        stats = requests.get(f"https://www.sumo-api.com/api/rikishi/{rikishi_id}/stats").json()
        info = (
            f"{shikona} | Wins: {stats['totalWins']} | Losses: {stats['totalLosses']} | "
            f"Bouts: {stats['totalMatches']} | Bashos: {stats['basho']} | Yusho: {stats['yusho']}"
        )
        ctx.reply(f"@{ctx.display_name} -> {info}")
    except Exception:
        ctx.reply(f"@{ctx.display_name} Error fetching record data.")
