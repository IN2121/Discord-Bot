#nya ichi ni san nya arigato!!!

VALID_GH_STRINGS = {"grubhub", "gh", "grub"}
VALID_VENMO_STRINGS = {"venmo", "venmo/zelle", "zelle/venmo", "v/z", "z/v", "v"}
VALID_ZELLE_STRINGS = {"zelle", "venmo/zelle", "zelle/venmo", "v/z", "z/v", "z"}


VENMO = "venmo"
ZELLE = "zelle"
BOTH = "venmo/zelle"

def isFloat(num):
    # string to float function, catches error if it does not work
    try:
        return float(num)
    except ValueError:
        return None
    
def newBlockRequestData():
    return {"platform": None, "price": None, "bumped": False, "grubhub": None}

def makeStringNice(str):
    return str.lower().strip()

def getDollarAmount(str):
    val = isFloat(str.replace("$", ""))
    if (val != None): return val
    else: return None

def representsPlatform(str):
    str = makeStringNice(str)
    # if either platform, return BOTH
    if (str in VALID_VENMO_STRINGS and 
        str in VALID_ZELLE_STRINGS): return BOTH
            
    #if its just in a single one, return just that one
    if (str in VALID_ZELLE_STRINGS): return ZELLE
    if (str in VALID_VENMO_STRINGS): return VENMO
    return None

def isGH(str):
    return (makeStringNice(str) in VALID_GH_STRINGS)


class BlockRequest:
    def __init__(self, message):
        self.message = message.lower()
        self.messageList = self.message.split()
        self.data = newBlockRequestData()
        self.useless = len(self.messageList) < 1
        self.request = None
        self.dm = None
        self.parse()

    #if for some dumbass reason we want to print our class :3
    def __str__(self):

        if (self.request):
            return f"Asking price is: {self.data["price"]}, with platform {self.data["platform"]}, and GH status is {self.data["grubhub"]}"
        else:
            return f"Message is not a request"
    
    def parse(self):

        if (self.useless): return
        
        for word in self.messageList:
            if (makeStringNice(word) == "dm"):
                self.dm = True
                break
            if (isGH(word)): 
                self.data["grubhub"] = True
                continue
            temp = representsPlatform(word)
            if (temp != None):
                self.data["platform"] = temp
                continue
            temp = getDollarAmount(word)
            if (temp != None):
                self.data["price"] = temp
                continue

        self.request = not (self.getPrice() == None and self.getPlatform() == None and self.isGH() == None)

    def getPrice(self):
        return self.data["price"]
    def getPlatform(self):
        return self.data["platform"]
    def isGH(self):
        return self.data["grubhub"]
    def isRequest(self):
        return self.request
        

