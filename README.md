# A discord bot for private osu! servers.
[Discord server](https://discord.gg/UqrbWKHHz3) for the emojis the bot uses (Recommended) 
## Change Log:
- ### 04/15/2023:
  - New:
    - Custom bot status that can be managed in `config.yml` and supports variables.
    - Improved logging and ability to manage logging settings in `config.yml`
  - Fixes:
    - Fixed `profile` command not working as expected when a username is given.
  - Misc.:
    - Added `config.yml` to .gitignore so pulling new updates will no longer require you to run `git stash` and lose your config
      - You'll have to run git stash once and pull for this change to reflect.
- ### 04/14/2023:
  - Added support for older bancho.py servers that does not have API versioning
    - Remove the value corresponding to `api_version` in `config.yml` to opt out from versioning
- ### 24/03/2023:
  - Improve general code readability and adaptation to PEP standards.
  - **Rewrote** `utils/api.py`:
    - It now uses separate variables to send requests to subdomains.
    - Supports exception handling for failing requests by raising `ValueError`.
    - Added API version support (managed in config.yml).
  - **Rewrote** `bot/cogs/osu.py`:
    - More readable, customizable and maintainable code in all commands.
    - Usernames can now be provided to commands that support it. Example: `!rs username ctb`
    - No longer uses users.json to store user IDs.
  - **New**: `utils/db.py`:
    - With the addition of `sqlitedict`, usage of JSON is no longer required to store user IDs and usernames.
    - Usernames are now stored in users.db, a file the bot will generate upon first start.
  - **Removed** `bot/cogs/sql.py`:
    - A barely used functionality with both vulnerability risks and constant connection failures is now fully removed.
    - *You're advised to remove your database credentials from your environment variables upgrading to this version*.

## Core Features:
- Link usernames to Discord user IDs
- View the latest score of a player
- View the detailed profile of a player
- View the server's leaderboard for any game mode including rx and ap leaderboards
- All game modes are supported in every command

## Commands
#### Arguments wrapped with square brackets are optional
- `!setuser <username>`
- `!leaderboard [mode]`
- `!profile [username] [mode]`
- `!rs [username] [mode]`

## Installation
- `git clone https://github.com/f11y11/nfuyu-bot.git`
- `pip install -r requirements.txt`
- `cp .env-template .env`
- `cp .config.yml-template .config.yml`
- Configure the bot settings and server domain in config.yml and set environment variables in .env
- Run the bot using `python main.py`

## Support (Contact Options)
- Discord @ fuyu#2302
- Email @ support@fuyu.gg
- [Discord Server](https://discord.gg/UqrbWKHHz3)
