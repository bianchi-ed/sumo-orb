import requests
from twitch.message_handler import commands

@commands.add(name="versus", aliases=[], cooldown=3)
def versus(ctx):
    if len(ctx.args) < 2:
        ctx.reply("Usage: !versus <rikishi1> <rikishi2>")
        return
    name1 = ctx.args[0].lower()
    name2 = ctx.args[1].lower()
    try:
        r = requests.get("https://www.sumo-api.com/api/rikishis")
        r.raise_for_status()
        rikishis = r.json()
        if not isinstance(rikishis, list):
            if isinstance(rikishis, dict) and "records" in rikishis and isinstance(rikishis["records"], list):
                rikishis = rikishis["records"]
            else:
                ctx.reply("API error: rikishi structure unexpected")
                return
        rikishi1 = next((rk for rk in rikishis if name1 == rk.get("shikonaEn", "").lower()), None)
        rikishi2 = next((rk for rk in rikishis if name2 == rk.get("shikonaEn", "").lower()), None)
        if not rikishi1 or not rikishi2:
            ctx.reply("Could not find one or both rikishis.")
            return
        id1 = rikishi1["id"]
        id2 = rikishi2["id"]
        url = f"https://www.sumo-api.com/api/rikishi/{id1}/matches/{id2}"
        v = requests.get(url)
        v.raise_for_status()
        data = v.json()
        wins = sum(data.get("kimariteWins", {}).values())
        losses = sum(data.get("kimariteLosses", {}).values())
        msg = f"@{ctx.display_name} -> {rikishi1['shikonaEn']} {wins} - {losses} {rikishi2['shikonaEn']}."
        # Print the last bout between the two
        matches = data.get("matches", [])
        if matches:
            last = matches[0]
            basho = last.get("bashoId", "?")
            if isinstance(basho, str) and len(basho) == 6 and basho.isdigit():
                basho_fmt = f"{basho[:4]}-{basho[4:]}"
            else:
                basho_fmt = basho
            day = last.get("day", "?")
            kimarite = last.get("kimarite", "?")
            winner = last.get("winnerEn", "?")
            loser = last.get("eastShikona") if last.get("winnerId") == last.get("westId") else last.get("westShikona")
            msg += f" Their last bout was at {basho_fmt} on day {day}. {winner} defeated {loser} by {kimarite}."
        ctx.reply(msg)
    except Exception as e:
        ctx.reply("Error fetching versus data.")
