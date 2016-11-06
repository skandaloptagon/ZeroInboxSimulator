import random
import json

deck = []
trash = []
players = []
winner = None
spaces = []
emails=["email reply","email attach","email meeting","email file"]

class player:
    deck = []
    space = 0

    def __init__(self, cards):
        self.deck = cards
        pass


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
            choice = random.choice([card for card in p.deck if not card.startswith("email")])
            p.deck.remove(choice)
            deck.append(choice)

            others = [player for player in players if player is not p]

            if choice == "forward":
                card = random.choice([card for card in p.deck if card.startswith("email")])
                target = random.choice(others)
                print "forwarding {} to {}".format(card,target)

            if choice == "reply all":
                for target in others:
                    try:
                        target.deck.append(deck.pop())
                    except:
                        random.shuffle(trash)
                        deck = trash
                        trash = []
                        target.deck.append(deck.pop())
                print "All players draw a card"

            if choice == "meeting request":
                target = random.choice(others)
                meeting = target
                boss = p

            if choice == "out of office":
                pass

            if choice == "server crash":
                pass
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

        #print "Player", i, "Moving..."
        #print i, "Landed on", p.space, spaces[p.space].card
        if spaces[p.space].draw:
            #print i, "Drawing Card..."
            try:
                p.deck.append(deck.pop())
            except:
                random.shuffle(trash)
                deck = trash
                trash = []
                p.deck.append(deck.pop())
        elif spaces[p.space].card == "free forward":
            #print "free forward"
            pass
        else:
            try:
                p.deck.remove(spaces[p.space].card)
                trash.append(spaces[p.space].card)
                #print i, "Got rid of", spaces[p.space].card
            except:
                pass

output = (str(len(players)),str(turns), str(rounds))
with open('output.tsv','a') as f:
    f.write( '\t'.join(output)+'\n')
