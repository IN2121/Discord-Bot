import discord
import parser
import json
import os
from dotenv import load_dotenv

# loads the enviornment file that stores the bot API key (very secret)
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

'''
Loads the intents for the bot
Intents let the bot read messages, join servers, and message back if needed
'''
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
intents.guilds = True           # Access server information
intents.guild_messages = True   # Receive messages from server channels

# Initialize the client with intents
client = discord.Client(intents=intents)

# global variabes 
# (things we save in a file and want to track) 
averagePrice = 0
offers = 0

# load data from data.json
def loadData():
    # use the global variables, don't make new ones
    global averagePrice, offers
    if (os.path.exists("data.json")):
        with open("data.json", "r") as f:
            # load the data from json
            data = json.load(f)

            # set the global variables equal to 
            # whatever was stored in the file 
            averagePrice = data.get("averagePrice", 0)
            offers = data.get("offers", 0)

# save the data within the file
def saveData():

    # make data equal to a set 
    # (dump takes care of the conversion)
    data = {
        "averagePrice": averagePrice,
        "offers": offers
    }
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

# just calculates new average price given a 
# new price ask (math is surely trivial :3 (I had to look it up NAHH >_<))
def calculateAveragePrice(price):
    global averagePrice, offers
    offers += 1
    if (offers == 1): averagePrice = price
    averagePrice = (averagePrice + price) / 2
   
# essentially a wrapper malloc call idk why I did this seems formal though
def newBlockRequest(message):
    return parser.BlockRequest(message)


# do this when the bot is loaded
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# do this whenever a new message is sent in a server the bot is in
@client.event
async def on_message(message):
    # Ignore messages from all bots (including itself)
    if message.author.bot: return

    if (message.channel.name == "block-market😋"):
        parsedMessage = newBlockRequest(message.content)
        price : int = parsedMessage.getPrice()
        platform : str  = parsedMessage.getPlatform()
        GH : bool = parsedMessage.isGH()
        calculateAveragePrice(price)
        saveData()
        print(f"Price is {price}, platform is {platform}, grubhub is {GH}")
        print(f"New average price is {averagePrice}")
    

# Run the bot
client.run(bot_token)