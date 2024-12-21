VALID_GH_STRINGS = {"grubhub", "gh", "grub"}
VALID_VENMO_STRINGS = {"venmo", "venmo/zelle", "zelle/venmo", "v/z", "z/v", "v"}
VALID_ZELLE_STRINGS = {"zelle", "venmo/zelle", "zelle/venmo", "v/z", "z/v", "z"}

VENMO = "venmo"
ZELLE = "zelle"
BOTH = "venmo/zelle"

class BlockRequest:
    def __init__(self, message):
        self.message = message
        self.messageList = self.message.split()
        self.platform = None
        self.price = None
        self.grubhub = None
        self.bumped = None

    #if for some dumbass reason we want to print our class
    def __str__(self):
        return f"Message: {self.message}, Platform: {self.platform}, Price: {self.price}"
    

    def getPrice(self):
        # if the price is already defined (not None)
        if (self.price != None): return self.price

        # havent gotten the price yet, gotta go throgh message and find it
        for word in self.messageList:
            # if there is a $ in the price, replace with empty, and return the int
            if ("$" in word): return int(word.replace("$", ""))
            # if its just a number return it (praying its the price)
            if (word.isdigit()): return int(word) 
    
        # hopefully should not reach here
        return None
    
    def getPlatform(self):
        # if already defined (why are you asking twice bro )
        if (self.platform != None): return self.platform

        for word in self.messageList:

            # if either platform, return BOTH
            if (word in VALID_VENMO_STRINGS and 
                word in VALID_ZELLE_STRINGS): return BOTH
            
            #if its just in a single one, return just that one
            if (word in VALID_ZELLE_STRINGS): return ZELLE
            if (word in VALID_VENMO_STRINGS): return VENMO

        return None
    
    def isGH(self):
        # if already initialized
        if (self.grubhub != None): return self.grubhub

        self.grubhub = False
        for word in self.messageList:
            if (word in VALID_GH_STRINGS): 
                self.grubhub = True
                found = True
                break
        return self.grubhub
        




        