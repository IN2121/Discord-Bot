import discord
import parser
import json
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Allow reading message content
intents.guilds = True           # Access server information
intents.guild_messages = True   # Receive messages from server channels

# Initialize the client with intents
client = discord.Client(intents=intents)

averagePrice = 0
offers = 0

def loadData():
    global averagePrice, offers
    if (os.path.exists("data.json")):
        with open("data.json", "r") as f:
            data = json.load(f)
            averagePrice = data.get("averagePrice", 0)
            offers = data.get("offers", 0)


def saveData():
    data = {
        "averagePrice": averagePrice,
        "offers": offers
    }
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

def calculateAveragePrice(price):
    global averagePrice, offers
    offers += 1
    if (offers == 1): averagePrice = price
    averagePrice = (averagePrice + price) / 2
   

def newBlockRequest(message):
    return parser.BlockRequest(message)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

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