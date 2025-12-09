import numpy as np
import random
from collections import defaultdict
import pickle

class Tetris:
    def __init__(self):
        self.width = 10
        self.height = 6
        self.board = np.zeros((self.height, self.width), dtype=int)
        self.current_piece = None
        self.game_over = False
        self.score = 0

        self.pieces = {
            'cuadrado': np.array([[1, 1], [1, 1]]),
            'L': np.array([[1, 0], [1, 0], [1, 1]]),
            'barra': np.array([[1], [1], [1], [1]]),
            'S': np.array([[0, 1, 1], [1, 1, 0]])
        }
    
    def reset(self):
        self.board = np.zeros((self.height, self.width), dtype=int)
        self.game_over = False
        self.score = 0
        return self.get_state()
    
    def get_random_piece(self):
        return random.choice(list(self.pieces.values()))
    
    def can_place(self, piece, col):
        if col < 0 or col + piece.shape[1] > self.width:
            return False, -1
        
      
        for row in range(self.height - piece.shape[0] + 1):
            if self._check_collision(piece, row, col):
                if row == 0:
                    return False, -1
                return True, row - 1
        
        return True, self.height - piece.shape[0]
    
    def _check_collision(self, piece, row, col):
        for i in range(piece.shape[0]):
            for j in range(piece.shape[1]):
                if piece[i, j] == 1:
                    if self.board[row + i, col + j] != 0:
                        return True
        return False
    
    def place_piece(self, piece, col):
        can, row = self.can_place(piece, col)
        if not can:
            self.game_over = True
            return -10  
        
        # Colocar pieza
        for i in range(piece.shape[0]):
            for j in range(piece.shape[1]):
                if piece[i, j] == 1:
                    self.board[row + i, col + j] = 1
        
 
        lines_cleared = self._clear_lines()
        
    
        reward = lines_cleared ** 2  
        if lines_cleared > 0:
            self.score += lines_cleared
        
        return reward
    
    def _clear_lines(self):
        lines = 0
        row = self.height - 1
        while row >= 0:
            if np.all(self.board[row] == 1):
                self.board[1:row+1] = self.board[0:row]
                self.board[0] = 0
                lines += 1
            else:
                row -= 1
        return lines
    
    def get_state(self):
        
        heights = []
        for col in range(self.width):
            h = 0
            for row in range(self.height):
                if self.board[row, col] == 1:
                    h = self.height - row
                    break
            heights.append(h)
        
       
        max_h = max(heights)
        diff = max(heights) - min(heights)
        holes = self._count_holes()
        
        return (tuple(heights), max_h, diff, holes)
    
    def _count_holes(self):
        holes = 0
        for col in range(self.width):
            found_block = False
            for row in range(self.height):
                if self.board[row, col] == 1:
                    found_block = True
                elif found_block and self.board[row, col] == 0:
                    holes += 1
        return holes
    
    def print_board(self):
        print("\n" + "="*22)
        for row in self.board:
            print("|" + "".join(["██" if cell else "  " for cell in row]) + "|")
        print("="*22)
        print(f"Score: {self.score}")


class QLearningAgent:
    def __init__(self, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
    
    def get_action(self, state, valid_actions):
        # Exploración vs explotación
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        
        # Elegir mejor acción
        q_values = {a: self.q_table[state][a] for a in valid_actions}
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]
        return random.choice(best_actions)
    
    def update(self, state, action, reward, next_state, valid_next_actions):
        current_q = self.q_table[state][action]
        
        if valid_next_actions:
            max_next_q = max([self.q_table[next_state][a] for a in valid_next_actions])
        else:
            max_next_q = 0
        
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state][action] = new_q
    
    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)
    
    def load(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = defaultdict(lambda: defaultdict(float), pickle.load(f))


def train_agent(episodes=1000, print_every=100):
    env = Tetris()
    agent = QLearningAgent(epsilon=0.3, alpha=0.5, gamma=0.9)
    
    scores = []
    
    for ep in range(episodes):
        state = env.reset()
        episode_reward = 0
        moves = 0
        
        while not env.game_over and moves < 100:
            piece = env.get_random_piece()
            
            
            valid_actions = []
            for col in range(env.width):
                can, _ = env.can_place(piece, col)
                if can:
                    valid_actions.append(col)
            
            if not valid_actions:
                break
            
            
            action = agent.get_action(state, valid_actions)
            
      
            reward = env.place_piece(piece, action)
            next_state = env.get_state()
            episode_reward += reward
            
        
            next_piece = env.get_random_piece()
            next_valid = []
            for col in range(env.width):
                can, _ = env.can_place(next_piece, col)
                if can:
                    next_valid.append(col)
            
            agent.update(state, action, reward, next_state, next_valid)
            
            state = next_state
            moves += 1
        
        scores.append(env.score)
        
        if (ep + 1) % print_every == 0:
            avg_score = np.mean(scores[-print_every:])
            print(f"Episodio {ep+1}/{episodes} - Score promedio: {avg_score:.2f}")
    
    return agent, scores


def play_game(agent, render=True):
    env = Tetris()
    state = env.reset()
    
    if render:
        env.print_board()
    
    moves = 0
    while not env.game_over and moves < 100:
        piece = env.get_random_piece()
        
        valid_actions = []
        for col in range(env.width):
            can, _ = env.can_place(piece, col)
            if can:
                valid_actions.append(col)
        
        if not valid_actions:
            break
        
     
        old_epsilon = agent.epsilon
        agent.epsilon = 0
        action = agent.get_action(state, valid_actions)
        agent.epsilon = old_epsilon
        
        env.place_piece(piece, action)
        state = env.get_state()
        
        if render:
            print(f"\nMovimiento {moves+1} - Columna: {action}")
            env.print_board()
            input("Presiona Enter para continuar...")
        
        moves += 1
    
    print(f"\nJuego terminado score final: {env.score}")
    return env.score


 
print("Entrenando agente...")
agent, scores = train_agent(episodes=500, print_every=100)

print("\nEntrenamiento completado")
print(f"Score promedio últimos 100 episodios: {np.mean(scores[-100:]):.2f}")

 
print("\n¿Ver una partida del agente entrenado? (s/n)")
if input().lower() == 's':
    play_game(agent, render=True)
else:
    
    test_scores = [play_game(agent, render=False) for _ in range(10)]
    print(f"\nScore promedio en 10 partidas: {np.mean(test_scores):.2f}")