import requests
from twitch.message_handler import commands

@commands.add(name="rikishi", aliases=[], cooldown=3)
def rikishi(ctx):
    if not ctx.args:
        ctx.reply(f"@{ctx.display_name} Usage: !rikishi <name>")
        return
    name_query = " ".join(ctx.args).lower()
    try:
        response = requests.get("https://www.sumo-api.com/api/rikishis")
        response.raise_for_status()
        rikishis = response.json()
    except Exception as e:
        ctx.reply(f"@{ctx.display_name} Error fetching rikishi data.")
        return
    if not isinstance(rikishis, list):
        if isinstance(rikishis, dict) and "records" in rikishis and isinstance(rikishis["records"], list):
            rikishis = rikishis["records"]
        else:
            ctx.reply(f"API response structure: {list(rikishis.keys())}")
            return
    found = None
    for rikishi in rikishis:
        if name_query == rikishi.get("shikonaEn", "").lower():
            found = rikishi
            break
    if not found:
        ctx.reply(f"@{ctx.display_name} No rikishi found for '{name_query}'.")
        return
    info = (
        f"Name: {found['shikonaEn']} | Rank: {found['currentRank']} | "
        f"Heya: {found['heya']} | Birth: {found['birthDate'][:10]} | Shusshin: {found['shusshin']} | "
        f"Height: {found['height']}cm | Weight: {found['weight']}kg | Debut: {found['debut']}"
    )
    ctx.reply(f"@{ctx.display_name} -> {info}")
