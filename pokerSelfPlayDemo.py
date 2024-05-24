from pokerClasses import PokerPlayer, PokerGame, Action
import random
class PokerUntilWinner:
    def __init__(self, players, smallBlind, buyin):
        self.players = players
        self.smallBlind = smallBlind
        self.buyin = buyin
        for player in self.players:
            player.budget = self.buyin
        self.startingPlayerIndex = 0
    
    def playUntilWinner(self):
        while self.areAllGamesOver() == False:
            print("New game started!")
            self.resetPlayers()
            self.shiftPlayers()
            self.playRound()
            # self.removePlayersWithNoMoney()
            print("One game ended!")
        print("Game over! " + str([player for player in self.players if player.budget > 0][0].id) + " won!")

    def resetPlayers(self):
        for player in self.players:
            player.resetValues()

    def shiftPlayers(self):
        self.startingPlayerIndex = (self.startingPlayerIndex + 1) % len(self.players)
        # self.players.append(self.players.pop(0))
    
    def playRound(self):
        pokerGame = PokerGame(self.players, self.smallBlind, self.startingPlayerIndex)
        while pokerGame.isGameOver() == False:
            print("###################")
            print("New round started! " + str(pokerGame.round))
            pokerGame.startRound()
            while pokerGame.isGameOver() == False and pokerGame.roundEnded() == False:
                player = pokerGame.getCurrentPlayer()
                print("-------------------")
                print("player.id", player.id, "budget", player.budget)
                print("player.id", player.id, "betted amount total", player.bettedAmount)
                print(pokerGame.getFlop())
                print(pokerGame.getPot())
                print(player)
                actions = pokerGame.getPlayerActions(player)
                print("actions", actions)
                rand = random.randint(0, len(actions) - 1)
                action = actions[rand]
                print("action", action)
                if(action == Action.RAISE):
                    raiseAmount = random.randint(pokerGame.getAmountToCall(player), player.budget)
                    pokerGame.playerTakeAction(player, action, raiseAmount)
                else:
                    pokerGame.playerTakeAction(player, action)
                print("-------------------")
            print(pokerGame.pot)
            pokerGame.finishRound()
        print("Round ended! " + str(pokerGame.round))
        print("###################")
        for player in self.players:
            print("player with id:" , player.id, "has", player.budget, player.hand)

    # def removePlayersWithNoMoney(self):
    #     players = []
    #     for player in self.players:
    #         if player.budget > 0:
    #             players.append(player)
    #     self.players = players
    #     print(self.players)
    
    def areAllGamesOver(self):
        return len([player for player in self.players if player.budget > 0]) == 1


player1 = PokerPlayer(1)
player2 = PokerPlayer(2)
player3 = PokerPlayer(3)
player4 = PokerPlayer(4)
player5 = PokerPlayer(5)

poker = PokerUntilWinner([player1, player2, player3, player4, player5], 10, 100)
poker.playUntilWinner()



# player1 = PokerPlayer(11, 1000)
# player2 = PokerPlayer(12, 1000)
# player3 = PokerPlayer(13, 1000)
# player4 = PokerPlayer(14, 1000)
# player5 = PokerPlayer(15, 1000)

# poker = PokerGame([player1, player2, player3, player4, player5], 10)

# while poker.isGameOver() == False:
#     print("New round started! " + str(poker.round))
#     poker.startRound()
#     while poker.roundEnded() == False:
#         player = poker.getCurrentPlayer()
#         print(poker.getFlop())
#         print(poker.getPot())
#         print(poker.getCurrentPlayer())
#         print(poker.getPlayerActions(poker.getCurrentPlayer()))
#         action = input("Action: ")
#         if action == "fold":
#             poker.playerTakeAction(player, Action.FOLD)
#         elif action == "call":
#             poker.playerTakeAction(player, Action.CALL)
#         elif action == "raise":
#             amount = int(input("Amount: "))
#             poker.playerTakeAction(player, Action.RAISE, amount)
#         elif action == "check":
#             poker.playerTakeAction(player, Action.CHECK)
#         elif action == "allin":
#             poker.playerTakeAction(player, Action.ALLIN)
#         else:
#             print("Invalid action")
#     poker.finishRound()
#     print("Round ended! " + str(poker.round))

# print("Game over!")
# print("The flop was: " + str(poker.flop))
# print("Player budgets:")
# for player in poker.players:
#     print("player with id:" , player.id, "has", player.budget, player.hand, "hand rank:", poker.getBestHand(player).rank)
