import discord
# import parser
import json
import os
from parser import BlockRequest
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
# initialize dictionary that stores all individual user requests
userData = dict()

VENMO = "venmo"
ZELLE = "zelle"
BOTH = "venmo/zelle"
OFFERS = "offers"
AVG_ASK_PRICE = "averageAskingPrice"
GH_REQS = "grubhubRequests"


DEFAULT_USER_DATA = {OFFERS: [], AVG_ASK_PRICE: 0.0, VENMO: 0, ZELLE: 0, GH_REQS: 0}


# load data from data.json
def loadData():
    # use the global variables, don't make new ones
    global averagePrice, offers, userData
    if (os.path.exists("data.json")):
        with open("data.json", "r") as f:
            # load the data from json
            data = json.load(f)

            # set the global variables equal to 
            # whatever was stored in the file 
            averagePrice = data.get("averagePrice", 0)
            offers = data.get("offers", 0)
            userData = data.get("userData", {})

# save the data within the file
def saveData():

    # make data equal to a set 
    # (dump takes care of the conversion)
    data = {
        "averagePrice": averagePrice,
        "offers": offers,
        "userData": userData
    }
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
    
def updateUserData(userID, blockRequest):
    if (userID not in userData):
        userData[userID] = DEFAULT_USER_DATA
    
    offer = blockRequest.getPrice()
    platform = blockRequest.getPlatform()
    gh = blockRequest.isGH()
    userInfo = userData[userID]


    userInfo[OFFERS].append(offer)
    if (gh): userInfo[GH_REQS] += 1
    if (platform == VENMO): userInfo[VENMO] += 1
    if (platform == ZELLE): userInfo[ZELLE] += 1
    if (platform == BOTH): 
        userInfo[VENMO] += 1
        userInfo[ZELLE] += 1

    if (userInfo[AVG_ASK_PRICE] == 0): 
        userInfo[AVG_ASK_PRICE] = offer
    else:
        userInfo[AVG_ASK_PRICE] = (userInfo[AVG_ASK_PRICE] + offer) / 2

    

# just calculates new average price given a 
# new price ask (math is surely trivial :3 (I had to look it up >_<))
def calculateAveragePrice(price):
    global averagePrice, offers
    offers += 1
    if (offers == 1): 
        averagePrice = price
        return
    averagePrice = (averagePrice + price) / 2
   
# essentially a wrapper malloc call idk why I did this seems formal though
def newBlockRequest(message):
    return BlockRequest(message)


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
        calculateAveragePrice(parsedMessage.getPrice())
        updateUserData(str(message.author.id), parsedMessage)
        saveData()
    

# Run the bot
client.run(bot_token)