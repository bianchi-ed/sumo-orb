import requests
from twitch.message_handler import commands

@commands.add(name="kimaritehistory", aliases=[], cooldown=3)
def kimarite(ctx):
    if not ctx.args:
        ctx.reply(f"@{ctx.display_name} Usage: !kimarite <kimarite name>")
        return
    kimarite_name = " ".join(ctx.args).lower()
    try:
        url = f"https://www.sumo-api.com/api/kimarite/{kimarite_name}"
        params = {"sortOrder": "desc", "limit": 1}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get("records") if isinstance(data, dict) else data
        if not records or not isinstance(records, list):
            ctx.reply(f"@{ctx.display_name} No matches found for kimarite '{kimarite_name}'.")
            return
        match = records[0]
        basho = match.get("bashoId", match.get("basho", "?"))
        if isinstance(basho, str) and len(basho) == 6 and basho.isdigit():
            basho_fmt = f"{basho[:4]}-{basho[4:]}"
        else:
            basho_fmt = basho
        day = match.get("day", "?")
        winner = match.get("winnerEn", match.get("winner", "?"))
        winner_id = match.get("winnerId")
        east_id = match.get("eastId")
        west_id = match.get("westId")
        east_shikona = match.get("eastShikona", "?")
        west_shikona = match.get("westShikona", "?")
        if winner_id == east_id:
            loser = west_shikona
        elif winner_id == west_id:
            loser = east_shikona
        else:
            loser = match.get("loserEn", match.get("loser", "?"))
        kimarite_used = match.get("kimarite", kimarite_name)
        match_no = match.get("matchNo", "?")
        ctx.reply(f"@{ctx.display_name} -> Last recorded {kimarite_used.title()}: {winner} defeated {loser} on {basho_fmt} day {day}, bout {match_no}.")
    except Exception:
        ctx.reply(f"@{ctx.display_name} -> Error fetching kimarite data.")
