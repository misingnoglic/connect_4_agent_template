import random

LARGE_NUMBER = 100000000

class ConnectFour:
    def __init__(self, width=7, height=6, connect_length=4):
        self.width = width
        self.height = height
        self.connect_length = connect_length
        self.cur_player = 1  # Players are 1 or -1
        self.board = self._generate_initial_state()
        self.move_history = []

    def _generate_initial_state(self):
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def to_move(self):
        return self.cur_player

    def print_cur(self, fancy=True):
        if fancy:
            print(self)
        else:
            print(self.board)

    def actions(self):
        return [col for col in range(self.width) if self.board[0][col] == 0]

    def apply_action(self, action):
        row = self.height - 1
        while row >= 0 and self.board[row][action] != 0:
            row -= 1
        if row < 0:
            return None
        self.board[row][action] = self.cur_player
        self.move_history.append((row, action))
        self.cur_player *= -1
        return self

    def undo_action(self):
        if not self.move_history:
            return None
        row, col = self.move_history.pop()
        self.board[row][col] = 0
        self.cur_player *= -1
        return self

    def result(self, action):
        return self.apply_action(action)

    def is_terminal(self):
        return self.is_win() or len(self.actions()) == 0
    
    def _check_win_rc(self, r, c):
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            count = 1
            for i in range(1, self.connect_length):
                nr, nc = r + dr * i, c + dc * i
                if 0 <= nr < self.height and 0 <= nc < self.width and self.board[nr][nc] == self.board[r][c]:
                    count += 1
                else:
                    break
            if count >= self.connect_length:
                return True
        return False

    def is_win(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] != 0:
                    if self._check_win_rc(r, c):
                        return True
        return False
    
    def utility(self, player):
        if self.is_win():
            return -LARGE_NUMBER if self.to_move() == player else LARGE_NUMBER
        elif self.is_terminal():
            return 0
        else:
            raise Exception('')
    
    def copy(self):
        new_board = ConnectFour(self.width, self.height, self.connect_length)
        new_board.board = [list(row) for row in self.board]
        new_board.cur_player = self.cur_player
        new_board.move_history = list(self.move_history)
        return new_board

    def simulate_move(self, action):
        new_game = self.copy()
        new_game.result(action)
        return new_game

    def get_board(self):
        return self.board

    def __str__(self):
        m = {0: "⚫️", -1: "🔴", 1: "🔵"}
        return "\n".join([" ".join([m[cell] for cell in row]) for row in self.board])
