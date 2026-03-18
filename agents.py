import abc
import random
import time

class Agent(abc.ABC):
    def __init__(self, name, time_limit=1.0):
        self.name = name
        self.time_limit = time_limit

    @abc.abstractmethod
    def get_action(self, game):
        pass

class HumanAgent(Agent):
    def _is_integer(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def get_action(self, game):
        print("Pick a move from the following legal moves via index or move name:")
        legal_moves = list(enumerate(game.actions()))
        for idx, move in legal_moves:
            print(f"{idx}: {move}")
        while True:
            choice = input("Enter your chosen move: ")
            if self._is_integer(choice):
                choice = int(choice)
                if 0 <= choice < len(legal_moves):
                    return legal_moves[choice][1]
                else:
                    print("Invalid index. Please try again.")
            else:
                for idx, move in legal_moves:
                    if str(move) == choice:
                        return move
                print("Invalid move name. Please try again.")

class RandomAgent(Agent):
    def get_action(self, game):
        valid_locations = game.actions()
        return random.choice(valid_locations)

def get_max_connected(game, r, c, player):
    game.board[r][c] = player
    max_count = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, game.connect_length):
            nr, nc = r + dr * i, c + dc * i
            if 0 <= nr < game.height and 0 <= nc < game.width and game.board[nr][nc] == player:
                count += 1
            else:
                break
        for i in range(1, game.connect_length):
            nr, nc = r - dr * i, c - dc * i
            if 0 <= nr < game.height and 0 <= nc < game.width and game.board[nr][nc] == player:
                count += 1
            else:
                break
        if count > max_count:
            max_count = count
    game.board[r][c] = 0
    return max_count

class HeuristicAgent(Agent):
    def get_action(self, game):
        valid_locations = game.actions()
        if not valid_locations:
            return None
            
        player = game.to_move()
        opponent = -player
        
        block_3 = []
        block_2 = []
        grow_3 = []
        grow_2 = []
        
        for col in valid_locations:
            # Find the row where the piece would land
            r = game.height - 1
            while r >= 0 and game.board[r][col] != 0:
                r -= 1
                
            # Check opponent's potential connections if they played here
            opp_connected = get_max_connected(game, r, col, opponent)
            # Check own potential connections if playing here
            own_connected = get_max_connected(game, r, col, player)
            
            if opp_connected >= 4:
                block_3.append(col)
            elif opp_connected >= 3:
                block_2.append(col)
            elif own_connected >= 4:
                grow_3.append(col)
            elif own_connected >= 3:
                grow_2.append(col)
                
        # Return based on priority buckets
        if block_3:
            return random.choice(block_3)
        if block_2:
            return random.choice(block_2)
        if grow_3:
            return random.choice(grow_3)
        if grow_2:
            return random.choice(grow_2)
            
        return random.choice(valid_locations)

class StudentAgent(Agent):
    def get_action(self, game):
        # Example of how to watch for the time limit
        # start_time = time.time()
        # while time.time() - start_time < self.time_limit:
        #     # Do some work
        #     # break if we run out of time
        #     pass
        
        valid_locations = game.actions()
        return random.choice(valid_locations)
