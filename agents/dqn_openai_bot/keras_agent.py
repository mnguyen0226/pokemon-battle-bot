# DQN agent with openai wrapper 
# Add in tensorboard

# https://keras-rl.readthedocs.io/en/latest/agents/dqn/
# https://poke-env.readthedocs.io/en/stable/rl_with_open_ai_gym_wrapper.html

import enum
from gym.core import Env
import numpy as np
from numpy import random
import tensorflow as tf

from poke_env.player.env_player import Gen8EnvSinglePlayer
from poke_env.player.random_player import RandomPlayer

# pip install keras-rl2
from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnneledPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.python.ops.gen_math_ops import Max

# Define RL Player
class SimpleRLPlayer(Gen8EnvSinglePlayer):
    def embed_battle(self, battle):

        # -1 indicates that the move does not have a base power 
        # or is not availabel
        moves_base_power = -np.ones(4)
        moves_dmg_multiplier = np.ones(4)

        for i, move in enumerate(battle.available_moves):
            moves_base_power[i] = (
                move.base_power / 100
            ) # Simple rescaling to facilitate learning

            if move.type:
                moves_dmg_multiplier[i] = move.type.damage_multiplier(
                    battle.opponent_active_pokemon.type_1,
                    battle.opponent_active_pokemon.type_2,
                )
        # Count number of pokemon have not fainted in each team
        remaining_mon_team = (
            len([mon for mon in battle.team.values() if mon.fainted]) / 6
        )

        remaining_mon_opponent = (
            len([mon for mon in battle.opponent_team.values() if mon.fainted]) / 6
        )

        # Finals vector with 10 components
        return np.concatenate(
            [
                moves_base_power,
                moves_dmg_multiplier,
                [remaining_mon_team, remaining_mon_opponent],
            ]
        )
        
    def compute_reward(self, battle) -> float:
        return self.reward_computing_helper(
            battle, fainted_value=2, hp_value=1, victory_value=30
        )

class MaxDamagePlayer(RandomPlayer):
    def choose_move(self, battle):
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

NUMBER_TRAINING_STEPS = 10000
NUMBER_EVALUATION_EPISODES = 100

tf.random.set_seed(0)
np.random.seed(0)

# This is the function that will be used to train the dqn
def dqn_training(player, dqn, nb_steps):
    dqn.fit(player, nb_steps=nb_steps)
    player.complete_current_battle()

def dqn_evaluation(player, dqn, nb_episodes):
    # Reset battle statistics
    player.reset_battles()
    dqn.test(player, nb_episodes=nb_episodes, visualize=False, verbose=False)

    print(f"DQN Evaluation: {player.n_won_batles} victories out of {nb_episodes} episodes")

def main():
    env_player = SimpleRLPlayer(battle_format="gen8randombattle")

    opponent = RandomPlayer(battle_format="gen8randombattle")
    second_opponent = MaxDamagePlayerbattle_format="gen8randombattle")

    # Output dimension
    n_action = len(env_player.action_space)

    model = Sequential()
    model.add(Dense(128, activation="relu", input_shape=(1, 10)))

    # Embedding layer has the shape (1, 10), which affects the hidden layer dimensions and output dimension
    # 





if __name__ == "__main__":
    main()