# minimax_agent.py
from agent_base import Agent
from game import GameState
import math
import time

class MinimaxAgent(Agent):
    def __init__(self):
        super().__init__()
        self.total_nodes = 0
        self.total_time = 0
        self.total_moves = 0
    
    def get_action(self, state: GameState, depth=None):
        start_time = time.time()#start the timer
        self.nodes_this_move = 0  # reset counter each move


        _, action = self.minimax(state)

        # this is to keep track of total nodes and time to later graph and compare between agents
        self.total_moves += 1
        self.total_nodes += self.nodes_this_move
        self.total_time += (time.time() - start_time)
        return action

    def minimax(self, state, depth_limit=None):
        self.nodes_this_move += 1  # count explored node

        """
        Returns: (value, best_action)
        
        TODO: Implement the minimax algorithm here.
        
        The algorithm should:
        1. Check if the state is terminal and return (utility, None) if so
        2. For MAX player ('X'): find the action that maximizes the minimum value
        3. For MIN player ('O'): find the action that minimizes the maximum value
        4. Recursively call minimax on successor states
        5. Return the best value and corresponding action as a tuple
        
        Hint: Use state.is_terminal(), state.utility(), state.get_legal_actions(),
              state.generate_successor(), and state.to_move
        """
        # TODO: Remove this line and implement the minimax algorithm
        if state.is_terminal():
            utility = state.utility()
            return (utility, None)
        
        best_action = None
        best_value = float(-math.inf) if state.to_move == 'X' else float(math.inf)

        for action in state.get_legal_actions():
            new_state = state.generate_successor(action)
            value, _ = self.minimax(new_state)

            if state.to_move == 'X':
                if value > best_value:
                    best_value = value
                    best_action = action
        
            else:
                if value < best_value:
                    best_value = value
                    best_action = action
        return (best_value, best_action)
    
    def __del__(self):
        if self.total_moves > 0:
            avg_nodes = self.total_nodes / self.total_moves
            avg_time = self.total_time / self.total_moves
            print("MinimaxAgent | AvgNodesPerMove =", avg_nodes, "| AvgTimePerMove =", avg_time, "s")
