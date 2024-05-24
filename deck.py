class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def __repr__(self):
        suits = {
            "S": "♠",
            "H": "♥",
            "D": "♦",
            "C": "♣",
        }
        ranks = {
            14: "A",
            11: "J",
            12: "Q",
            13: "K",
        }
        if self.rank in ranks:
            rank = ranks[self.rank]
        else:
            rank = str(self.rank)
        return f"{rank}{suits[self.suit]}"
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    def __lt__(self, other):
        return self.rank < other.rank
    def __hash__(self):
        return hash((self.rank, self.suit))

class CardDeck:
    def __init__(self):
        self.deck = [Card(rank, suit) for rank in range(2, 15) for suit in "SHDC"]
    def __repr__(self):
        return str(self.deck)
    def __len__(self):
        return len(self.deck)
    def __getitem__(self, position):
        return self.deck[position]
    def shuffleCards(self):
        import random
        random.shuffle(self.deck)
    def drawCards(self, n):
        return [self.deck.pop() for i in range(n)]
    def numCards(self):
        return len(self.deck)
