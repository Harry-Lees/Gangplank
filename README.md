# Gangplank
A League of Legends bot

## About the project

Gangplank is a League of Legends bot written in Python for looking at your League of Legends stats without
leaving your Discord server. This bot provides Champion, Summoner and Match History information provided
by the Riot API.

## Commands

prefix = !

* chests <summoner> - Shows champions with available chests for the given summoner. (sorted by highest mastery)
* match_history <summoner> - Shows the last 10 matches in the given summoners match history.
* status - Shows the status of League of Legends.
* profile - Shows the given summoners profile.

## Getting Started

To run this bot, may self-host or use our hosted link (recommended)

### Self Hosting

#### Prerequisites

In order to run this bot, you will need to provide your own Discord token as-well as a Riot API key. These may be provided in the form of a .env file in the src/ directory. Please create the file in the format below (replace <your token here> with the token/ api-key).

```
DISCORD_BOT_TOKEN=<your bot token here>
RIOT_API_KEY=<your api key here>
```

After creating the .env file you may run the bot.


#### Docker

Provided you have Docker installed, you may run the Dockerfile with the following commands.

```
docker build -t gangplank_image -f Dockerfile .
docker run -d --name gangplank_bot gangplank_image
```

Running `docker ps` should show the Docker process running with the name "gangplank".

#### Running from command line

To run the project without Docker, you will need Python 3 installed. To install the requirements for this project, you may use the command.

```
python3 -m pip install -r requirements.txt
```

after installing the dependancies, you may run the bot by navigating to the src/ directory and running 

```
python3 main.py
```

The following message should appear:

```
Logged in as
Gangplank Bot
<your_token_here>
------------
```

## Contributing

There are currently no contributing guidelines, however all help is appreciated. If you would like to discuss ideas, you may open an Issue to discuss, if you would like to contribute code, you may create a Pull Request for review.

## License

This project is distributed under the MIT License. See `LICENSE` for more information.