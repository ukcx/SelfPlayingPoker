from pokerClasses import PokerPlayer
from pokerClasses import PokerGame
from pokerClasses import Action
from deck import Card

import gym
import random
from gym import spaces
import numpy as np

class PokerEnv(gym.Env):
    def __init__(self, num_players, small_blind, buyin):
        super(PokerEnv, self).__init__()
        self.num_players = num_players
        self.small_blind = small_blind
        self.buyin = buyin
        self.players = [PokerPlayer(i, self.buyin) for i in range(self.num_players)]
        for player in self.players:
            player.budget = self.buyin
        # Observation space initialization
        self.observation_space = self._create_observation_space()

        # Action space initialization
        self.action_space = self._create_action_space()

    def restart(self, num_players, small_blind, buyin):
        self.num_players = num_players
        self.small_blind = small_blind
        self.buyin = buyin
        self.players = [PokerPlayer(i, self.buyin) for i in range(self.num_players)]
        for player in self.players:
            player.budget = self.buyin
        # Observation space initialization
        self.observation_space = self._create_observation_space()

        # Action space initialization
        self.action_space = self._create_action_space()
    
    def _create_observation_space(self):
        # Calculate initial observation space shape
        observation_space_shape = self._get_observation_space_shape()
        return spaces.Box(low=0, high=1, shape=(observation_space_shape,), dtype=np.float32)

    def _create_action_space(self):
        return spaces.Discrete(5)  # 0: fold, 1: call, 2: raise, 3: check, 4: all-in 
    # spaces.Tuple((
    #         spaces.Discrete(5),  # 0: fold, 1: call, 2: raise, 3: check, 4: all-in
    #         spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)  # Continuous action for raise amount
    #     ))
    def resetPlayers(self):
        for player in self.players:
            player.resetValues()

    def shiftPlayers(self):
        return

    def removePlayersWithNoMoney(self):
        # Remove players with no money from the game
        # self.players = [player for player in self.players if player.budget > 0]
        # Update the number of players in the observation space
        #self.observation_space = self._create_observation_space()
        return
    
    def areAllGamesOver(self):
        return len([player for player in self.players if player.budget > 0]) == 1

    def _get_observation_space_shape(self):
        # Budget, current bet, folded, all-in, hand (2 cards) for each player
        player_info_length = 4 + 2 * 2
        community_cards_length = 5 * 2  # Up to 5 community cards
        return self.num_players * player_info_length + community_cards_length + 3  # Pot size, current round, amount to call

    def reset(self):
        # self.removePlayersWithNoMoney()
        self.resetPlayers()
        # self.shiftPlayers()
        if self.areAllGamesOver():
            return self._get_state()
        self.round = PokerGame(self.players, self.small_blind)
        self.round.startRound()
        return self._get_state()
    
    def _get_default_hand(self):
        return [Card(2, 'S'), Card(2, 'H')]

    def _get_state(self):
        state = []
        for player in self.players:
            state.extend([player.budget / self.buyin, player.bettedAmount / self.buyin])
            state.append(1 if player.isFolded() else 0)
            state.append(1 if player.isAllIn else 0)
            hand = player.hand if len(player.hand) == 2 else self._get_default_hand()
            state.extend(self._encode_hand(hand))
            print("player", self.round.getCurrentPlayer())
            print("player.hand", player.hand)
        
        print("flop", self.round.getFlop())
        state.extend(self._encode_hand(self.round.getFlop()))
        state.extend([0] * (5 - len(self.round.getFlop())) * 2)
        
        state.append(self.round.getPot() / (self.buyin * self.num_players))
        state.append(self.round.round / 4)
        
        current_player = self.round.getCurrentPlayer()
        amount_to_call = self.round.getAmountToCall(current_player) / self.buyin
        state.append(amount_to_call)
        
        return np.array(state, dtype=np.float32)

    def _encode_hand(self, hand):
        card_values = []
        for card in hand:
            card_values.append(card.rank / 14)
            card_values.append(self._encode_suit(card.suit))
        return card_values
    
    def _encode_suit(self, suit):
        suit_dict = {'S': 0.25, 'H': 0.5, 'D': 0.75, 'C': 1.0}
        return suit_dict[suit]

    def getCurrentPlayer(self):
        return self.round.getCurrentPlayer()

    def step(self, action):
        if self.areAllGamesOver():
            return self._get_state(), self._calculate_reward, True, {}
        discrete_action = action
        # discrete_action, raise_fraction = action
        raise_fraction = 0.5  # Fraction of the budget to raise by
        current_player = self.round.getCurrentPlayer()
        actions = self.round.getPlayerActions(current_player)

        if discrete_action not in actions:
            discrete_action = actions[random.randrange(0, len(actions))]
        
        if discrete_action == Action.RAISE:  # If the action is 'raise'
            min_raise = self.round.getAmountToCall(current_player)
            max_raise = current_player.getBudget()
            raise_amount = min_raise + raise_fraction * (max_raise - min_raise)
            chosen_action = (Action.RAISE, raise_amount)
        else:
            chosen_action = discrete_action
        
        if isinstance(chosen_action, tuple):
            action_type, amount = chosen_action
            self.round.playerTakeAction(current_player, action_type, amount)
        else:
            self.round.playerTakeAction(current_player, chosen_action)
        
        if self.round.roundEnded():
            print("round ended")
            self.round.finishRound()
            # if self.round.isGameOver():
            #     return self._get_state(), self._calculate_reward(current_player), True, {}
            self.round.startRound()

        done = self.round.isGameOver() or self.areAllGamesOver()
        print("done", done)
        reward = self._calculate_reward(current_player)
        
        return self._get_state(), reward, done, {}

    def _calculate_reward(self, player):
        return player.getBudget()  # Simple reward based on the player's budget

    def render(self, mode='human'):
        pass
