from twitch.message_handler import commands, PREFIX

@commands.add(name="commands", aliases=[""], cooldown=5)
def help_command(ctx):
    ctx.reply(f"@{ctx.display_name} -> Commands: {', '.join(PREFIX + c for c in commands.list())}. For a comprehensive list of commands and usage examples visit www.sumo-orb.com")
