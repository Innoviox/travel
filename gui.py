import parse

import random
import sys
import time

import tkinter as tk

#Initialize globals
global selected_card, cardToPut, changedAPile, rack, root, won, dp, d
won = False #if the rack was valid
selected_card = None #the current card that is selected
cardToPut = None #the card from the top of the deck
changedAPile = False #if the user has already drawn a card
rack = None #the global rack
dp = None #the global discard pile
d = None #the global draw pile

#Constants
CARD_TO_PUT_X = 250
CARD_TO_PUT_Y = 125
CARD_WIDTH = 100
CARD_HEIGHT = 50

class Card(parse.Piece):
    def __init__(self, *args):
        super().__init__(*args[:3])
        root, x, y, frame, w, h, index, fa, a, b= args[3:]
        self.__forcea = fa
        global dp, d
        self.dp = pileCreate(dp)
        self.d = pileCreate(d)
        self.index = index
        self.root = root
        self.rackFrame = frame
        self.x = x
        self.y = y

        
        self.w = w
        self.h = h


        self.text = self.name

        self.getFrame(w, h)
        self.label.bind('<ButtonPress-1>', self.select)
        self.frame.bind('<ButtonPress-1>', self.select)
        self.frame.index = self.index
        self.frame.full = self
        self.selected = False

    def getFrame(self, w, h):
        self.frame = tk.Frame(self.rackFrame, bd=1, relief=tk.SUNKEN)
        self.frame.pack_propagate(False)
        self.frame.place(x=self.x, y=self.y, width=w, height=h)   
        self.label = tk.Label(self.frame, bd=1, relief=tk.RAISED, \
                           text=self.text,  
                           height=w, width=h, bg=self.color)
        self.label.pack(fill=tk.X, padx=1, pady=1)

    def select(self, *event):
        global selected_card
        if self.selected:
            selected_card = None
        else:
            selected_card = self
            global cardToPut
            if cardToPut is not None:
                swap(self, cardToPut, False or self.__forcea, self.dp)

class EmptyCard(Card):
    def __init__(self, *args):
        super().__init__(*args)
    def select(self, *event):
        pass
    def _update(self):
        pass

class Rack(tk.Frame):
    def __init__(self, root, x, y, dp, d, rack = []):
        super().__init__(root, relief=tk.SUNKEN, bd=2)
        self.place(x=x, y=y, width=CARD_WIDTH*10, height=CARD_HEIGHT)
        self.cards = rack
        self.root = root
        self.dp = dp
        self.d = d
        i=0
        while len(self.cards) < 10 and len(d.cardsIn) > 0:
            b = random.choice(d.cardsIn)
            if b.type == parse.C:
                c = parse.createC(b.name)
            else:
                c = parse.createT(b.name, b.color)
            d.cardsIn.remove(b)
            self.cards.append(c)
            i+=1
        self.cardActuals = []
        for (i,c) in enumerate(self.cards):
            self.cardActuals.append(Card(c.name, c.type, c.color, self.root, i*CARD_WIDTH, 0, self, CARD_WIDTH, CARD_HEIGHT, i, False, dp, d))
    def getRack(self):
        rack = [0] * 10
        for tile in self.winfo_children():
            if isinstance(tile.index, int):
                rack[tile.index] = tile.full
        return rack
def pileCreate(o):
    return o#Pile(o.root, o.x, o.y, o.showTop, o.name, o.addable, o.cards)

class Pile(tk.Frame):
    def __init__(self, root, x, y, showTop, name, addable, cards = []):
        super().__init__(root, relief=tk.SUNKEN, bd=2)
        self.root = root
        self.x = x
        self.y = y
        self.cards = cards
        self.place(x=x, y=y, width=100, height=100)
        self.cardsIn = cards
        self.showTop = showTop
        self.name = name
        #print("initalizing", self.name)
        self.showTopCard()
        self.label.bind('<ButtonPress-1>', self.select)
        self.bind('<ButtonPress-1>', self.select)
        self.addable = addable
    def showTopCard(self):
        #print("cards in", self.name, self.cardsIn)
        try:
            self.label
        except AttributeError:
            self.label = tk.Label(self, bd=1, relief=tk.RAISED, \
                               text=self.name,  
                               height=50, width=50, bg="white")            
        if len(self.cardsIn):
            if self.showTop:
                #print("showing card", self.cardsIn[-1], "on", self.name)
                self.label.config(text=self.cardsIn[-1].text,bg=self.cardsIn[-1].color)
            else:
                #print("hiding card", self.cardsIn[-1], self.name)
                self.label.config(text="Top Card",bg="white")
        else:
            #print("no cards in", self.name)
            self.label.config(text=self.name, bg="white")

        self.label.pack(fill=tk.X, padx=1, pady=1)
        self.label.lift()

    def addCard(self, card, a):
        #print("added card", card, "to", self.name)
        self.cardsIn.append(card)
        if a:empty(card)
        #card.frame.destroy()
        #print("SHOWING CARD FROM ADDCARD", self.name)
        self.showTopCard()

    def putCard(self):
        try:
            global cardToPut
            if cardToPut is None:
                cardToPut = self.cardsIn[-1]
                self.cardsIn.remove(self.cardsIn[-1])#self.cardsIn.pop(-1)
                #print("cards in", self.name, self.cardsIn)
                forcePutCard()
                #print("forced card from", self.name)
                #print("SHOWING CARD FROM PUTCARD", self.name)
                self.showTopCard()
                global changedAPile
                changedAPile = True
        except IndexError:
            print("Can't draw", file=sys.stderr)
            
    def select(self, *event):
        #print("selected", self.name)
        global selected_card, changedAPile
        if not changedAPile:
            #print("putting card from", self.name)
            self.putCard()
        else:
            print("Can't draw from", self.name, file=sys.stderr)

def forcePutCard():
    global cardToPut, rack
    c=cardToPut
    cardToPut = Card(c.name, c.type, c.color, root, CARD_TO_PUT_X, CARD_TO_PUT_Y, root, CARD_WIDTH, CARD_HEIGHT, "empty", True, rack.dp, rack.d)

def swap(card1, card2, a, dp):
    x1, y1, i1 = card1.x, card1.y, card1.index
    x2, y2, i2 = card2.x, card2.y, card2.index
    card1.frame.place_configure(x=x2, y=y2)
    card2.frame.place_configure(x=x1, y=y1)
    card2.index = i1
    card1.index = i2
    card2.frame.index = i1
    card1.frame.destroy()
    card2.frame.update()
    card2.rackFrame = card1.rackFrame
    discard(card1, a, dp)
    
def discard(card, a, dp):
    #print("discarding", card)
    dp.addCard(card, a)
    #card.frame.destroy()
    exitGui()


def exitGui():
    global rack, r, dp, d
    dp = rack.dp
    d = rack.d
    r = rack.getRack()
    if isinstance(cardToPut.index, int):
        r[cardToPut.index] = cardToPut
    print("Your rack is", r)
    if parse.valid(r):
        print("You Win!")
        global won
        won = True
    else:
        print("Not yet...")
    root.destroy()

def empty(card):
    global rack
    empty = EmptyCard("empty", "empty", "white", root, card.x, card.y, root, CARD_WIDTH, CARD_HEIGHT, "empty", True, rack.dp, rack.d)

           
def gui(discardCards, bag, tiles):
    global rack, root, changedAPile, cardToPut, dp, d
    cardToPut = None
    changedAPile = False
    
    root = tk.Tk()
    root.geometry("{}x1000+0+0".format(CARD_WIDTH*10))

    discardPile = dp = Pile(root, 0, 100, True, "Discard Pile", True, discardCards)
    deck = d = Pile(root, 100, 100, False, "Deck", False, bag)
    rack = Rack(root, 0, 0, discardPile, deck, tiles)
    
    img = tk.PhotoImage(file='america.gif')
    _map = tk.Label(root, image=img)
    _map.img = img
    _map.place_configure(x=0, y=210)

    root.mainloop()

if __name__ == "__main__":
    gui([], parse.createBag(), [])
