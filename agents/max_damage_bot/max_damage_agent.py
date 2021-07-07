import asyncio
from poke_env.player.player import Player

class MaxDamagePlayer(Player):
    """ Class has one abstract method choose_move
    """

async def main():
    """Bot will attack and use the move with the highest base power if the active 
    pokemon can attack. Else, the pokemon will perform random actions
    """
    # The player that we implement does not need to be trained so we can inherit from Player class
    

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())