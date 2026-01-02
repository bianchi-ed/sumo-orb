import requests
from twitch.message_handler import commands

RANK_ORDER = ["Yokozuna","Ozeki","Sekiwake","Komusubi","Maegashira","Juryo","Makushita","Sandanme","Jonidan","Jonokuchi"]

def get_rank_index(rank_str):
    for i, rank in enumerate(RANK_ORDER):
        if rank.lower() in rank_str.lower():
            return i
    return len(RANK_ORDER)

@commands.add(name="highestrank", aliases=[], cooldown=3)
def highestrank(ctx):
    if not ctx.args:
        ctx.reply(f"@{ctx.display_name} Usage: !highestrank <rikishi name>")
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
                ctx.reply("API error: rikishi structure unexpected")
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
                ctx.reply("API error: matches structure unexpected")
                return
        highest_rank = None
        highest_index = len(RANK_ORDER)
        rikishi_id_str = str(rikishi_id)
        for match in matches:
            if str(match.get("eastId")) == rikishi_id_str:
                rank_str = match.get("eastRank", "")
            elif str(match.get("westId")) == rikishi_id_str:
                rank_str = match.get("westRank", "")
            else:
                continue
            idx = get_rank_index(rank_str)
            if idx < highest_index:
                highest_index = idx
                highest_rank = rank_str
        try:
            rikishi_resp = requests.get(f"https://www.sumo-api.com/api/rikishi/{rikishi_id}")
            rikishi_resp.raise_for_status()
            rikishi_data = rikishi_resp.json()
            current_rank = rikishi_data.get("currentRank", "")
            idx_current = get_rank_index(current_rank)
            if idx_current < highest_index:
                highest_index = idx_current
                highest_rank = current_rank
        except Exception:
            pass
        if highest_rank:
            ctx.reply(f"@{ctx.display_name} -> {highest_rank}")
        else:
            ctx.reply(f"@{ctx.display_name} -> No rank data found for the specified rikishi.")
    except Exception as e:
        ctx.reply("Error fetching data.")
