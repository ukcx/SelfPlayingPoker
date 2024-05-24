from deck import CardDeck

class PokerHand:
    def __init__(self, cards):
        self.cards = cards
        self.cards.sort()
        self.cards.reverse()
        self.rank = self.getRank()
    def __repr__(self):
        return str(self.cards)
    def __len__(self):
        return len(self.cards)
    def __getitem__(self, position):
        return self.cards[position]
    def getRank(self):
        if self.isRoyalFlush():
            return 10
        elif self.isStraightFlush():
            return 9
        elif self.isFourOfAKind():
            return 8
        elif self.isFullHouse():
            return 7
        elif self.isFlush():
            return 6
        elif self.isStraight():
            return 5
        elif self.isThreeOfAKind():
            return 4
        elif self.isTwoPair():
            return 3
        elif self.isPair():
            return 2
        else:
            return 1.0 * self.cards[0].rank / 14
    def isRoyalFlush(self):
        if self.isStraightFlush() and self.cards[0].rank == 14:
            return True
        else:
            return False
    def isStraightFlush(self):
        if self.isFlush() and self.isStraight():
            return True
        else:
            return False
    def isFourOfAKind(self):
        if self.cards[0].rank == self.cards[3].rank or self.cards[1].rank == self.cards[4].rank:
            return True
        else:
            return False
    def isFullHouse(self):
        if self.isThreeOfAKind() and self.isPair():
            return True
        else:
            return False
    def isFlush(self):
        if self.cards[0].suit == self.cards[1].suit == self.cards[2].suit == self.cards[3].suit == self.cards[4].suit:
            return True
        else:
            return False
    def isStraight(self):
        if self.cards[0].rank == self.cards[1].rank + 1 == self.cards[2].rank + 2 == self.cards[3].rank + 3 == self.cards[4].rank + 4:
            return True
        else:
            return False
    def isThreeOfAKind(self):
        if self.cards[0].rank == self.cards[2].rank or self.cards[1].rank == self.cards[3].rank or self.cards[2].rank == self.cards[4].rank:
            return True
        else:
            return False
    def isTwoPair(self):
        if self.cards[0].rank == self.cards[1].rank and self.cards[2].rank == self.cards[3].rank:
            return True
        elif self.cards[0].rank == self.cards[1].rank and self.cards[3].rank == self.cards[4].rank:
            return True
        elif self.cards[1].rank == self.cards[2].rank and self.cards[3].rank == self.cards[4].rank:
            return True
        else:
            return False
    def isPair(self):
        if self.cards[0].rank == self.cards[1].rank or self.cards[1].rank == self.cards[2].rank or self.cards[2].rank == self.cards[3].rank or self.cards[3].rank == self.cards[4].rank:
            return True
        else:
            return False

from enum import Enum

class Action(Enum):
    FOLD = 0
    CALL = 1
    RAISE = 2
    CHECK = 3
    ALLIN = 4

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, Action):
            return self.value == other.value
        return False

print(Action.FOLD == 0)  # Now this will print True


class PokerGame:
    def __init__(self, players, smallBlind):
        self.deck = CardDeck()
        self.deck.shuffleCards()
        self.flop = []
        self.players = players
        self.smallBlind = smallBlind
        self.round = 0
        self.roundBet = 0
        self.pot = 0
        self.playersTurn = 0
        self.playersLeft = len(self.players)
        self.playersLeftToPlayInThisRound = len(self.players)
        print("num players", len(self.players))
        for player in self.players:
            if player.getBudget() == 0:
                print( "herer")
                player.folded = True
        self.nonFoldedPlayers = [player for player in self.players if player.folded == False]
        print(len(self.nonFoldedPlayers))
    
    def startRound(self):
        for player in self.players:
            player.resetRoundBet()
        self.roundBet = 0
        if self.round == 0:
            self.handleCards(2)
            self.makeInitialBets()
        elif self.round == 1:
            self.flopCards(3)
        elif self.round == 2:
            self.flopCards(1)
        elif self.round == 3:
            self.flopCards(1)
        self.playersLeftToPlayInThisRound = self.playersLeft
    
    def makeInitialBets(self):
        while(self.players[self.playersTurn].folded):
            self.playerTakeAction(self.players[self.playersTurn], Action.FOLD)
        if self.players[self.playersTurn].getBudget() <= self.smallBlind:
            self.playerTakeAction(self.players[self.playersTurn], Action.ALLIN)
        else:
            self.playerTakeAction(self.players[self.playersTurn], Action.RAISE, self.smallBlind)
        
        while(self.players[self.playersTurn].folded):
            self.playerTakeAction(self.players[self.playersTurn], Action.FOLD)
        if self.players[self.playersTurn].getBudget() <= self.smallBlind * 2:
            self.playerTakeAction(self.players[self.playersTurn], Action.ALLIN)
        else:
            self.playerTakeAction(self.players[self.playersTurn], Action.RAISE, self.smallBlind * 2)
    
    def finishRound(self):
        self.round += 1
        if self.isGameOver():
            self.getWinner()
    
    def getAmountToCall(self, player):
        return self.roundBet - player.roundBet
    
    def getPlayerActions(self, player): #all in fix needed
        if player.isFolded() == False:
            if player.isAllIn:
                return [Action.CHECK]
            if self.getAmountToCall(player) == 0:
                return [Action.FOLD, Action.RAISE, Action.ALLIN, Action.CHECK]
            elif player.getBudget() <= self.getAmountToCall(player):
                return [Action.FOLD, Action.ALLIN]
            else:
                return [Action.FOLD, Action.CALL, Action.RAISE, Action.ALLIN]
        else:
            return [Action.FOLD]
    
    def playerTakeAction(self, player, action, amount = 0):
        if self.playersTurn != self.players.index(player):
            raise ValueError
        if action == Action.FOLD:
            self.playerFold(player)
        elif action == Action.CALL:
            self.playerCall(player)
        elif action == Action.RAISE:
            self.playerRaise(player, amount)
        elif action == Action.CHECK:
            self.playerCheck(player)
        elif action == Action.ALLIN:
            self.playerAllIn(player, player.getBudget())
    
    def getCurrentPlayer(self):
        return self.players[self.playersTurn]

    def roundEnded(self):
        if self.playersLeftToPlayInThisRound == 0:
            return True
        else:
            return False
    
    def nextPlayer(self):
        self.playersTurn += 1
        if self.playersTurn == len(self.players):
            self.playersTurn = 0
        # if self.playersTurn == lastPlayer:
        #     self.finishRound()
    
    def playerRaise(self, player, amount):
        try:
            player.bet(amount)
            self.pot += amount
            self.roundBet = player.roundBet
            self.playersLeftToPlayInThisRound = len(self.players) - 1
            self.nextPlayer()
        except ValueError:
            print("Not enough money")
    
    def playerCall(self, player):
        try:
            amount = self.getAmountToCall(player)
            player.bet(amount)
            self.pot += amount
            self.playersLeftToPlayInThisRound -= 1
            self.nextPlayer()
        except ValueError:
            print("Not enough money")
    
    def playerCheck(self, player):
        try:
            if not player.isAllIn and self.getAmountToCall(player) != 0:
                raise ValueError
            self.playersLeftToPlayInThisRound -= 1
            self.nextPlayer()
        except ValueError:
            print("Not enough money")
    
    def playerAllIn(self, player, amount):
        try:
            player.bet(amount)
            self.pot += amount
            self.roundBet = max(player.roundBet, self.roundBet)
            self.playersLeftToPlayInThisRound = len(self.players) - 1
            self.nextPlayer()
        except ValueError:
            print("Not enough money")
    
    def playerFold(self, player):
        player.fold()
        self.playersLeftToPlayInThisRound -= 1
        if self.playersLeft != 1:
            self.nextPlayer()
    
    def getWinner(self):
        nonFoldedPlayers = [player for player in self.players if player.isFolded() == False]
        winner = nonFoldedPlayers[0]
        if len(nonFoldedPlayers) == 1:
            winner.budget += self.pot
            print(winner)
            return winner
        roundBets = [player.getBettedAmount() for player in self.players]
        while max(roundBets) != 0:
            winner = nonFoldedPlayers[0]
            winnerBestHand = self.getBestHand(winner)
            for player in nonFoldedPlayers:
                playerBestHand = self.getBestHand(player)
                if playerBestHand.rank > winnerBestHand.rank:
                    winner = player
                    winnerBestHand = playerBestHand
            winnerBet = winner.getBettedAmount()
            if winnerBet == max(roundBets):
                winner.budget += self.pot
                break
            else:
                for player in self.players:
                    amountWonOverThisPlayer = min(player.getBettedAmount(), winnerBet)
                    winner.budget += amountWonOverThisPlayer
                    player.bettedAmount -= amountWonOverThisPlayer
                    self.pot -= amountWonOverThisPlayer
            nonFoldedPlayers = [player for player in self.players if player.bettedAmount > 0]
            roundBets = [player.getBettedAmount() for player in self.players]
        return winner
    
    def getBestHand(self, player):
        import itertools
        bestHand = PokerHand(self.flop)
        for comb in itertools.combinations(player.hand + self.flop, 5):
            comb = list(comb)
            if PokerHand(comb).rank > bestHand.rank:
                bestHand = PokerHand(comb)
        return bestHand
    
    def isGameOver(self):
        if self.round == 4 or len([player for player in self.players if not player.isFolded()]) == 1:
            return True
        else:
            return False
    
    def handleCards(self, n):
        for player in self.players:
            player.hand = self.deck.drawCards(n)
    
    def flopCards(self, n):
        self.flop = self.flop + self.deck.drawCards(n)
    
    def getFlop(self):
        return self.flop
    
    def getPot(self):
        return self.pot



class PokerPlayer:
    def __init__(self, id, budget=0):
        self.id = id
        self.budget = budget
        self.bettedAmount = 0
        self.roundBet = 0
        self.hand = []
        self.folded = False
        self.isAllIn = False
    def getBudget(self):
        return self.budget
    def getBettedAmount(self):
        return self.bettedAmount
    def bet(self, amount):
        if(amount > self.budget):
            raise ValueError("You don't have enough money to bet that much!")
        self.roundBet += amount
        self.budget -= amount
        self.bettedAmount += amount
        if self.budget == 0:
            self.isAllIn = True
    def resetValues(self):
        self.bettedAmount = 0
        self.roundBet = 0
        self.hand = []
        self.folded = False
        self.isAllIn = False
    def resetRoundBet(self):
        self.roundBet = 0
    def isFolded(self):
        return self.folded
    def fold(self):
        self.folded = True
    def __repr__(self):
        return str(self.hand)
    def __len__(self):
        return len(self.hand)
    def __getitem__(self, position):
        return self.hand[position]

