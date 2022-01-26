## busta
Discord bot that will join and play their intro song

## Deployment
This application is deployed to Replit. It also makes use of the Replit database

## Install dependencies 
Run `pip install -r requirements.txt` in the root directory (or `pip3`)

## Environment setup
Use a `.env` file for discord tokens. The file should look like this

    TOKEN=mydiscordtoken
    REPLIT_DB_URL=replit_database_url
    
### To get a discord token
   [Discord guide to creating and getting your discord token](https://discordpy.readthedocs.io/en/stable/discord.html)

### To get a replit database URL
1. Create a repl in [Replit](https://replit.com/)
2. In the shell tab, type in the shell `echo $REPLIT_DB_URL`
    
## Running
Run `py main.py` in root directory
