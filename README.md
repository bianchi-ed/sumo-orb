## sumo-orb

This bot provides sumo wrestling info and stats in Twitch chat. Use the commands below:

### Commands & Examples

**!whois <username>**
Shows Twitch info about a user.
> Example: `!whois sumo_orb`
> 
> @user -> [ Username: sumo_orb ] [ ID: 123456 ] [ Broadcaster: affiliate ] [ Created: 01/01/2020 ] [ Profile Pic: https://... ]

**!rikishi <name>**
Shows info about a rikishi.
> Example: `!rikishi onosato`
> 
> @user -> Name: Onosato | Rank: Yokozuna 1 East | Heya: Onomatsu | Birth: 2000-12-01 | Shusshin: Ishikawa | Height: 190cm | Weight: 170kg | Debut: 202003

**!highestrank <name>**
Shows the highest rank ever achieved by a rikishi.
> Example: `!highestrank onosato`
> 
> @user -> Yokozuna 1 East

**!record <name>**
Shows the total win-loss record, number of matches, and bashos for a rikishi.
> Example: `!record onosato`
> 
> @user -> Onosato: 50W-20L | Matches: 70 | Bashos: 12

**!versus <rikishi1> <rikishi2>**
Shows the head-to-head record between two rikishis.
> Example: `!versus onosato hoshoryu`
> 
> @user -> Onosato 3 - 3 Hoshoryu

**!help**
Lists all available commands.
> Example: `!help`
> 
> @user -> Commands: !whois, !rikishi, !highestrank, !record, !versus, !help