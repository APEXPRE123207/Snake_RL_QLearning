import pyglet
import torch
import random
import numpy as np
from collections import deque
from snake import Direction, SnakeGameAI, Point
from model import Linear_QNet, QTrainer
from plotter import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    
    def __init__(self):
        self.no_of_games = 0
        self.epsilon = self.epsilon = max(0.01, 0.8 * (0.99 ** self.no_of_games))  # randomness
        self.gamma = 0.9  # discount rate less than 1 ONLY
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(11, 256, 3)  # neural network
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)  # optimizer

    def get_state(self, game):
        data = game.get_game_data()
        head = data["head"]
        food = data["food"]
        direction = data["direction"]
        #print(f"head: {head}, food: {food}, direction: {direction}")
        point_left = Point(head.x - 20, head.y)
        point_right = Point(head.x + 20, head.y)
        point_up = Point(head.x, head.y - 20)
        point_down = Point(head.x, head.y + 20)

        dir_left = direction == Direction.LEFT
        dir_right = direction == Direction.RIGHT
        dir_up = direction == Direction.UP
        dir_down = direction == Direction.DOWN

        state = [
            #Danger straight
            (dir_right and game.is_collision(point_right)) or
            (dir_left and game.is_collision(point_left)) or
            (dir_up and game.is_collision(point_up)) or
            (dir_down and game.is_collision(point_down)),

            #Danger right
            (dir_up and game.is_collision(point_right)) or
            (dir_down and game.is_collision(point_left)) or
            (dir_left and game.is_collision(point_up)) or
            (dir_right and game.is_collision(point_down)),

            #Danger left
            (dir_down and game.is_collision(point_right)) or
            (dir_up and game.is_collision(point_left)) or
            (dir_right and game.is_collision(point_up)) or
            (dir_left and game.is_collision(point_down)),

            dir_left,
            dir_right,
            dir_up,
            dir_down,

            food.x < head.x,
            food.x > head.x,
            food.y < head.y,
            food.y > head.y,

            
        ]
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.no_of_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            #print("Move: ",move)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)  # [0.5, 0.3, 0.9]
            prediction = self.model(state0)  # prediction [0.1, 0.5, 0.9] #This executes the forward function in model.py
            move = torch.argmax(prediction).item()  # it will return index of largest value
            #print("_______NEW_________")
            #print("Move: ",move)
            final_move[move] = 1

        return final_move

class TrainingManager:
    def __init__(self, update_interval=1 / 60.0):
        """
        Initializes the TrainingManager.
        
        :param update_interval: Interval (in seconds) between training steps.
        """
        self.plot_scores = []
        self.plot_mean_scores = []
        self.total_score = 0
        self.record = 0
        self.agent = Agent()
        self.game = SnakeGameAI()
        self.training_done = False
        self.update_interval = update_interval

    def load_model(self, model_path="model.pth"):
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()  # Set the model to evaluation mode
        print(f"Model loaded from {model_path}")

    def train_step(self, dt):
        """
        Executes a single training step. Called at regular intervals by pyglet.
        """
        if self.training_done:
            return

        # Get the current state of the game
        state_old = self.agent.get_state(self.game)

        # Decide the next action based on the current state
        final_move = self.agent.get_action(state_old)
        #print("Final_Move ",final_move)
        # Perform the action in the game
        reward, done, score = self.game.update(final_move)
        state_new = self.agent.get_state(self.game)

        # Train the agent's short-term memory
        self.agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Store the experience in memory
        self.agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Handle game over, reset game, and update stats
            self.handle_game_over(score)

    def handle_game_over(self, score):
        """
        Handles the end of a game, resets, and updates metrics.
        """
        self.game.reset()
        self.agent.no_of_games += 1
        self.agent.train_long_memory()

        if score > self.record:
            self.record = score
            self.agent.model.save()

        # Logging and statistics
        print(f'Game {self.agent.no_of_games}  Score: {score}  Record: {self.record}')
        self.plot_scores.append(score)
        self.total_score += score
        mean_score = self.total_score / self.agent.no_of_games
        self.plot_mean_scores.append(mean_score)
        plot(self.plot_scores, self.plot_mean_scores)

    def run(self):
        """
        Starts the pyglet event loop for the training manager.
        """
        pyglet.clock.schedule_interval(self.train_step, self.update_interval)  # Schedule training steps
        pyglet.app.run()  # Run the main event loop

if __name__ == '__main__':
    # Instantiate and run the TrainingManager
    manager = TrainingManager(update_interval=1 / 60.0)  # Adjust update_interval as needed
    manager.run()