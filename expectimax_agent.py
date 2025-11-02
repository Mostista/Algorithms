# expectimax_agent.py
from agent_base import Agent
from game import GameState
from evaluation import betterEvaluationFunction
import math
import time

class ExpectimaxAgent(Agent):
    def __init__(self):
        super().__init__()
        self.total_nodes = 0
        self.total_time = 0
        self.total_moves = 0
    
    def get_action(self, state: GameState, depth=None):
        start_time = time.time()
        self.nodes_this_move = 0  # reset counter each move
        """
        Returns the best move index (0-8) using Expectimax search.
        Handles stochastic (non-optimal) opponent moves.
        """
        value, action = self.expectimax(state, depth_limit=depth, current_depth=0)
        # this is to keep track of total nodes and time to later graph and compare between agents
        self.total_moves += 1
        self.total_nodes += self.nodes_this_move
        self.total_time += (time.time() - start_time)
        # Safety fallback in case no action is found
        if action is None:
            legal = state.get_legal_actions()
            if legal:
                action = legal[0]
        return action

    def expectimax(self, state: GameState, depth_limit, current_depth):
        """
        Recursive Expectimax returning (value, best_action)
        
        TODO: Implement the expectimax algorithm here.
        
        The algorithm should:
        1. Check if the state is terminal and return (utility, None) if so
        2. Check if depth limit is reached and use heuristic evaluation if so
        3. For MAX node ('X'): find the action that maximizes expected value
        4. For CHANCE node ('O'): calculate expected value by averaging over all possible actions
           (assumes opponent plays randomly with uniform probability)
        5. Return the value and best action as a tuple
        
        Hint: For chance nodes, you'll need to average the values of all successor states.
              Use betterEvaluationFunction(state) for non-terminal cutoff evaluation.
        """
        # Terminal check
        if state.is_terminal():
            return state.utility(), None

        # Cutoff check
        if depth_limit is not None and current_depth >= depth_limit:
            return betterEvaluationFunction(state), None

        # TODO: Implement the expectimax algorithm logic here
        # Remove this line and implement the algorithm
        legal_actions = state.get_legal_actions()
        if state.to_move == 'X':
            best_value = float(-math.inf)
            best_action = None

            for action in legal_actions:
                new_state = state.generate_successor(action)
                value, _ = self.expectimax(new_state, depth_limit, current_depth + 1)

                if value > best_value:
                    best_value = value
                    best_action = action
            return (best_value, best_action)
        
        else:
            num_actions = len(legal_actions)
            if num_actions == 0:
                return state.utility(), None
            
            sum_of_values = 0
            for action in legal_actions:
                new_state = state.generate_successor(action)
                value, _ = self.expectimax(new_state, depth_limit, current_depth + 1)
                sum_of_values += value

            expected_value = sum_of_values / num_actions
            return (expected_value, None)

    def __del__(self):
        if self.total_moves > 0:
            avg_nodes = self.total_nodes / self.total_moves
            avg_time = self.total_time / self.total_moves
            print("ExpectimaxAgent | AvgNodesPerMove =", avg_nodes, "| AvgTimePerMove =", avg_time, "s")
        else:
            print("ExpectimaxAgent | No moves made.")