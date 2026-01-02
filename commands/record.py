import requests
from twitch.message_handler import commands

@commands.add(name="record", aliases=[], cooldown=3)
def record(ctx):
    if not ctx.args:
        ctx.reply(f"@{ctx.display_name} Usage: !record <rikishi name>")
        return
    name_query = " ".join(ctx.args).lower()
    try:
        r = requests.get("https://www.sumo-api.com/api/rikishis")
        r.raise_for_status()
        rikishis = r.json()
        if not isinstance(rikishis, list):
            if isinstance(rikishis, dict) and "records" in rikishis and isinstance(rikishis["records"], list):
                rikishis = rikishis["records"]
            else:
                ctx.reply(f"@{ctx.display_name} API error: rikishi structure unexpected")
                return
        found = None
        for rikishi in rikishis:
            if name_query == rikishi.get("shikonaEn", "").lower():
                found = rikishi
                break
        if not found:
            ctx.reply(f"@{ctx.display_name} No rikishi found for '{name_query}'.")
            return
        rikishi_id = found["id"]
        m = requests.get(f"https://www.sumo-api.com/api/rikishi/{rikishi_id}/matches")
        m.raise_for_status()
        matches = m.json()
        if not isinstance(matches, list):
            if isinstance(matches, dict) and "records" in matches and isinstance(matches["records"], list):
                matches = matches["records"]
            else:
                ctx.reply(f"@{ctx.display_name} API error: matches structure unexpected")
                return
        wins = 0
        losses = 0
        bashos = set()
        rikishi_id_str = str(rikishi_id)
        total_matches = 0
        for match in matches:
            if str(match.get("eastId")) == rikishi_id_str or str(match.get("westId")) == rikishi_id_str:
                total_matches += 1
                basho_id = match.get("bashoId")
                if basho_id:
                    bashos.add(basho_id)
                if str(match.get("winnerId")) == rikishi_id_str:
                    wins += 1
                else:
                    losses += 1
        ctx.reply(f"@{ctx.display_name} -> {found['shikonaEn']} record: {wins} (W) - {losses} (L) | Total Bouts: {total_matches} | Total Bashos: {len(bashos)}")
    except Exception as e:
        ctx.reply(f"@{ctx.display_name} -> Error fetching record data.")
