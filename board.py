import random

def roll_d6():
    roll = random.randint(1,1)
    print "\trolled {}".format(roll)
    return roll

def draw_card(player, board):
    if len(board.cards) == 0:
        board.shuffle_trash()

    player.cards.append(board.draw_card())

class board:
    players = dict()
    spaces = dict()
    cards = []
    trash = []
    winner = None

    def __init__(self):
        pass

    def add_player(self, player):
        self.players[player]=0

    def add_space(self,no,title):
        self.spaces[no]=title

    def add_card(self, card):
        self.cards.append(card)

    def trash_card(self, card):
        self.trash.append(card)

    def shuffle_trash(self):
        self.cards = self.trash
        self.trash = []

    def draw_card(self):
        index = random.randint(0,len(self.cards)-1)
        card = self.cards[index]
        self.cards.remove(card)
        return card

    def move_player(self, player):
        prior=self.players[player]
        self.players[player]+=roll_d6()
        print "\tMoved from {} to {}".format(prior,self.players[player])
        if self.players[player] != self.players[player]%44 and len(player.cards)==0:
            self.winner = player
        self.players[player]=self.players[player]%44
    
    def process_space(self,player):
        space = self.players[player]
        if self.spaces[space] == "reply":
            if "email reply" in player.cards:
                player.cards.remove("email reply")
                self.trash.append("email reply")
                print "\t",player.name,"emailed reply",str(len(player.cards)),"cards remain"
                return
        if self.spaces[space] == "send attachment":
            if "email attach" in player.cards:
                player.cards.remove("email attach")
                elf.trash.append("email attach")
                print "\t",player.name,"sent attachment",str(len(player.cards)),"cards remain"
                return
        if self.spaces[space] == "schedule meeting":
            if "email meeting" in player.cards:
                player.cards.remove("email meeting")
                elf.trash.append("email meeting")
                print "\t",player.name,"scheduled meeting",str(len(player.cards)),"cards remain"
                return
        if self.spaces[space] == "file away":
            if "email file" in player.cards:
                player.cards.remove("email file")
                elf.trash.append("email file")
                print "\t",player.name,"filed away",str(len(player.cards)),"cards remain"
                return
        
class card:
    
    def __init__(self, name):
        self.name = name

class player:

    name = ""
    cards = []

    def __init__(self,name):
        self.name = name
        pass    

if __name__ == "__main__":
    zi = board()

    zi.add_space(0,"refresh inbox / start")
    zi.add_space(1,"reply")
    zi.add_space(2,"send attachment")
    zi.add_space(3,"inbox alert")
    zi.add_space(4,"schedule meeting")
    zi.add_space(5,"file away")
    zi.add_space(6,"inbox alert")
    zi.add_space(7,"file away")
    zi.add_space(8,"inbox alert")
    zi.add_space(9,"send attachment")
    zi.add_space(10,"reply")
    zi.add_space(11,"free forward")
    zi.add_space(12,"file away")
    zi.add_space(13,"schedule meeting")
    zi.add_space(14,"inbox alert")
    zi.add_space(15,"send attachment")
    zi.add_space(16,"inbox alert")
    zi.add_space(17,"send attachment")
    zi.add_space(18,"reply")
    zi.add_space(19,"inbox alert")
    zi.add_space(20,"file away")
    zi.add_space(21,"schedule meeting")
    zi.add_space(22,"free forward")
    zi.add_space(23,"send attachment")
    zi.add_space(24,"reply")
    zi.add_space(25,"inbox alert")
    zi.add_space(26,"file away")
    zi.add_space(27,"schedule meeting")
    zi.add_space(28,"inbox alert")
    zi.add_space(29,"reply")
    zi.add_space(30,"inbox alert")
    zi.add_space(31,"schedule meeting")
    zi.add_space(32,"send attachment")
    zi.add_space(33,"free forward")
    zi.add_space(34,"file away")
    zi.add_space(35,"reply")
    zi.add_space(36,"inbox alert")
    zi.add_space(37,"schedule meeting")
    zi.add_space(38,"inbox alert")
    zi.add_space(39,"reply")
    zi.add_space(40,"send attachment")
    zi.add_space(41,"inbox alert")
    zi.add_space(42,"schedule meeting")
    zi.add_space(43,"file away")

    p0 = player("one")
    p1 = player("two")
    p2 = player("three")
    p3 = player("four")
    p4 = player("five")
    p5 = player("six")
    p6 = player("seven")
    p7 = player("eight")

    for i in range(10):
        zi.add_card(card("email reply"))
        zi.add_card(card("email attach"))
        zi.add_card(card("email meeting"))
        zi.add_card(card("email file"))

    zi.add_player(p0)
    zi.add_player(p1)
    zi.add_player(p2)
    zi.add_player(p3)
    zi.add_player(p4)
    zi.add_player(p5)
    zi.add_player(p6)
    zi.add_player(p7)

    print zi.players
    print zi.spaces

    for i in range(3):
        for player in zi.players:
            draw_card(player,zi)

    while zi.winner is None:
        print "Winner: " + str(zi.winner)
        for player in zi.players:
            print "player {}'s turn".format(player.name)
            zi.move_player(player)
            zi.process_space(player)
    
    print "The winner is " + zi.winner.name
    
    print len(zi.cards)
