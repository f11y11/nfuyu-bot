# A discord bot for private osu! servers.
[Discord server](https://discord.gg/fuZy7MUh7Y) for the emojis the bot uses (Recommended) 

## Core Features:
- Save player usernames in a local sqlite database (no setup needed)
- View top and latest plays of a player in any game mode
- View the detailed profile of a player in any game mode
- View the server's leaderboard for any game mode including rx and ap leaderboards
- All game modes are supported in every command

## Commands
- `!setuser <username>`
- `!leaderboard [mode]`
- `!osutop|maniatop|taikotop|taikorxtop|ctbtop|ctbrxtop|rxtop|aptop [username] [mode]`
- `!rs [username] [mode]`
- `!osu|std|mania|ctb|ctbrx|taiko|taikorx|rx|ap`
- `!stats`

<sup>Arguments wrapped with &lt;angle brackets&gt; are required and arguments wrapped with [square brackets] are optional</sup>

## Installation
- Download the [latest release](https://github.com/f11y11/nfuyu-bot/releases/latest) or clone the repository <sub>`git clone https://github.com/f11y11/nfuyu-bot.git`</sub>
- Install the dependencies <sub>`pip install -r requirements.txt`</sub>
- Copy the contents of `.env-template` into `.env` <sub>`cp .env-template .env`</sub>
- Copy the contents of `config.yml-template` into `config.yml` <sub>`cp config.yml-template config.yml`</sub>
- Copy the contents of `templates.yml-template` into `templates.yml` <sub>`cp templates.yml-template templates.yml`</sub>
- Configure the bot settings and server domain in `config.yml` and add your bot token in `.env`
- You can customize the bot's responses in `templates.yml`
- Run `main.py` to start the bot. <sub>`python main.py`</sub>

## Contact / Support
- [Send an email](mailto:support@fuyu.gg)
- [Discord Server](https://discord.gg/fuZy7MUh7Y)

<sub>Looking for change logs? They are now shared with each [release](https://github.com/f11y11/nfuyu-bot/releases)</sub>
# <img src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.png" width="25" alt="JetBrains Logo (Main) logo."> <img src="https://resources.jetbrains.com/storage/products/company/brand/logos/PyCharm_icon.png" width="25" alt="PyCharm logo.">
