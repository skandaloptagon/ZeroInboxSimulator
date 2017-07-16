import random
import json

deck = []
trash = []
players = []
winner = None
spaces = []
emails=["email reply","email attach","email meeting","email file"]

player_number = 1
class player:
    deck = []
    space = 0
    name = ""

    def __init__(self, cards):
        global player_number
        self.deck = cards
        self.name = "Player {}".format(player_number)
        player_number += 1
        pass

    def __str__(self):
        return self.name


class space:
    draw = False

    def __init__(self, card, draw=False):
        self.draw = draw
        self.card = card

with open("board.json") as board:
    s = board.read()
    #print s
    obj = json.loads(s)
    #print obj

    email_deck = []

    for card in obj["deck"]:
        if card["name"].startswith("email"):
            email_deck.extend([card["name"]]*card["amount"])
        else:
            deck.extend([card["name"]]*card["amount"])

    print deck
    print len(email_deck)


    for i in range(8):
        temp_deck=[]
        for j in range(3):
            temp_deck.append(email_deck.pop())
            print len(email_deck)
        players.append(player(temp_deck))

    for i in players:
        print i.deck

    deck.extend(email_deck)
    
    for i in obj["board"]:
        try:
            #print i["draw"]
            spaces.append(space(i["card"],draw=i["draw"]))
        except:
            try:
                spaces.append(space(i["name"],draw=i["draw"]))
            except:
                spaces.append(space(i["name"]))


def cycle_trash(p):
    global deck, trash
    if len(deck) > 0:
        p.deck.append(deck.pop())
    else:
        random.shuffle(trash)
        deck = trash
        trash = []
        if len(deck) > 0:
            p.deck.append(deck.pop())
        else:
            pass

def forward(p):
    others = [player for player in players if player is not p]
    try:
        card = random.choice([card for card in p.deck if card.startswith("email")])
        target = random.choice(others)
        if in_office(target):
            p.deck.remove(card)
            target.deck.append(card)
            print "forwarding {} to {}".format(card,target)
    except IndexError:
        pass 

def in_office(p):
    if "out of office" in p.deck:
        p.deck.remove("out of office")
        print "{} is out of office".format(p)
        return False
    return True

random.shuffle(deck)

winner = False
turns = 0
rounds = 0
while not winner:
    i = 0
    rounds+=1

    meeting = None
    boss = None

    for p in set(players)-set([meeting]):
        #TODO: Play a card

        if boss is p:
            meeting = None
            boss = None

        try:
            # player chooses an action card (not an email) or reaction (out of office) 
            choice = random.choice([card for card in p.deck if not card.startswith("email") and not card == "out of office" ])
            
            # remove the chosen card from the players deck and append it to the primary deck
            p.deck.remove(choice)
            deck.append(choice)

            #others is a list of players that is not the current player
            others = [player for player in players if player is not p]


            # Here I process the players action card choice

            if choice == "forward":
                forward(p)

            elif choice == "reply all":
                print "All players draw a card"
                for target in others:
                    cycle_trash(target)

            elif choice == "meeting request":
                target = random.choice(others)
                if in_office(target):
                    meeting = target
                    boss = p

                    print "{} request a meeting with {}".format(boss,target)

            elif choice == "server crash":
                print "Server crashed: killing all cards from this player"
                for card in p.deck:
                    if card.startswith("email"):
                        print "\tRemoving card {}".format(card)
                        p.deck.remove(card)
                        deck.append(card)

            else:
                print "player had no choices"

        except:
            pass

        #Roll and process space
        turns += 1
        i += 1
        p.space += random.randint(1,6)
        if p.space >= 44 and any(x in emails for x in p.deck):
            print "We have a winner!!!"
            winner = True
            break
        p.space = p.space%len(spaces)

        if spaces[p.space].draw:
            cycle_trash(p)

        elif spaces[p.space].card == "free forward":
            forward(p)
            pass
        else:
            # Discard Space Card
            try:
                p.deck.remove(spaces[p.space].card)
                trash.append(spaces[p.space].card)
                #print i, "Got rid of", spaces[p.space].card
            except:
                pass

output = (str(len(players)),str(turns), str(rounds))
with open('output.tsv','a') as f:
    f.write( '\t'.join(output)+'\n')
