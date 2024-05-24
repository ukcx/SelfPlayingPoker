from pokerEnv import PokerEnv
import sys
print(sys.version)

import torch

if torch.cuda.is_available():
    print("CUDA is available. You can use GPU acceleration.")
else:
    print("CUDA is not available. You can only use CPU.")

from stable_baselines3.common.callbacks import BaseCallback

class EarlyStoppingCallback(BaseCallback):
    def __init__(self, check_func, verbose=0):
        super(EarlyStoppingCallback, self).__init__(verbose)
        self.check_func = check_func

    def _on_step(self) -> bool:
        # Call the environment's areAllGamesOver function
        if self.check_func():
            print("Early stopping condition met. Training terminated.")
            return False  # Returning False stops training
        return True  # Continue training

import gym
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

# Define the parameters
num_players = 4
small_blind = 10
buyin = 1000
num_episodes = 1000

# Create the environment
env = DummyVecEnv([lambda: PokerEnv(num_players, small_blind, buyin)])
early_stopping_callback = EarlyStoppingCallback(env.envs[0].areAllGamesOver)

# Define and train the agent
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=num_episodes, callback=early_stopping_callback)

# Save the trained model
model.save("poker_model")
print("Model saved successfully.")
model.env.envs[0].restart(num_players, small_blind, buyin)

# Evaluate the trained agent
total_rewards = [0 for _ in range(num_players)]
for _ in range(10):
    obs = env.reset()
    if env.envs[0].areAllGamesOver():
        break
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        total_rewards[env.envs[0].getCurrentPlayer().id] += reward

print("Total rewards:", total_rewards)
print("Average total reward:", np.mean(total_rewards))

# Load the saved model
loaded_model = PPO.load("poker_model")

# Continue using the loaded model if needed