import requests
from twitch.message_handler import commands

@commands.add(name="bashoresults", aliases=[], cooldown=3)
def bashoresults(ctx):
    if not ctx.args:
        ctx.reply(f"@{ctx.display_name} Usage: !bashoresults <bashoId YYYY-MM>")
        return
    basho_id = ctx.args[0]
    if not ('-' in basho_id and len(basho_id) == 7 and basho_id[:4].isdigit() and basho_id[5:].isdigit() and basho_id[4] == '-'): 
        ctx.reply(f"@{ctx.display_name} Usage: !bashoresults <bashoId YYYY-MM>")
        return
    api_basho_id = basho_id.replace('-', '')
    try:
        api_basho_id = basho_id.replace('-', '')
        url = f"https://www.sumo-api.com/api/basho/{api_basho_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        yusho = data.get("yusho", [])
        prizes = data.get("specialPrizes", [])
        yusho_str = ", ".join(f"{x['shikonaEn']} ({x['type']})" for x in yusho) if yusho else "None"
        from collections import defaultdict
        prize_map = defaultdict(list)
        for p in prizes:
            prize_map[p['type']].append(p['shikonaEn'])
        if prize_map:
            prizes_str = " | ".join(f"{ptype}: {', '.join(names)}" for ptype, names in prize_map.items())
        else:
            prizes_str = "None"
        msg = f"@{ctx.display_name} -> Yusho: {yusho_str}"
        if prizes_str != "None":
            msg += f" | {prizes_str}"
        ctx.reply(msg)
    except Exception:
        ctx.reply(f"@{ctx.display_name} -> Error fetching basho results.")
