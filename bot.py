import discord
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
DM_ATTEMPTS = "DMAttempts"
PREFIX = "!"

def get_new_user_default():
    return {OFFERS: [], AVG_ASK_PRICE: 0.0, VENMO: 0, ZELLE: 0, GH_REQS: 0, DM_ATTEMPTS: 0}


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

def updateUserData(userID, blockRequest : BlockRequest):

    if (userID not in userData):
        userData[userID] = get_new_user_default()

    userInfo = userData[userID]

    if (blockRequest.isRequest()):

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
            numOffers = len(userInfo[OFFERS])
            userInfo[AVG_ASK_PRICE] = ((userInfo[AVG_ASK_PRICE] * (numOffers - 1)) + offer) / numOffers
        
    elif (blockRequest.dm):
        userInfo[DM_ATTEMPTS] += 1

def getUserData(userID):
    if (userID not in userData):
        return None
    return userData[userID]



# just calculates new average price given a 
# new price ask (math is surely trivial :3 (I had to look it up >_<))
def calculateAveragePrice(price):
    global averagePrice, offers
    if (offers == 0):
        averagePrice = price
    else:
        averagePrice = ((averagePrice * offers) + price) / (offers + 1)
    offers += 1

def isBotCommand(str):
    return str[0] == PREFIX

def getCommand(str):
    return str.split()[0]

# do this when the bot is loaded
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    loadData()

# do this whenever a new message is sent in a server the bot is in
@client.event
async def on_message(message):
    # Ignore messages from all bots (including itself)
    if message.author.bot: return

    if message.content.strip() == "": return

    if (isBotCommand(message.content)):
        command = getCommand(message.content[1:])
        userData = getUserData(str(message.author.id))
        if (userData == None):
            await message.channel.send("Oops! Looks like you've never sent anything!")
            return
        if (command == "data"):
            string = f'''Your average asking price is {userData[AVG_ASK_PRICE]}
                    Number of venmo offers is {userData[VENMO]}
                    Number of zelle offers is {userData[ZELLE]}
                    Number of offers with grubhub is {userData[GH_REQS]}
                    Total DM attempts are {userData[DM_ATTEMPTS]}
                    '''
            await message.channel.send(string)
        elif (command == "offers"):
            string = f"Here is a dump of all your previous block offers! {userData[OFFERS]}"
            await message.channel.send(string)



    if (message.channel.name == "block-market😋"):
        msg = BlockRequest(message.content)
        print(msg)
        if (msg.isRequest()):
            calculateAveragePrice(msg.getPrice())
        updateUserData(str(message.author.id), msg)
        saveData()

# Run the bot
client.run(bot_token)
