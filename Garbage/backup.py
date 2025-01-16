import pyglet
import random
from enum import Enum
from collections import namedtuple
import numpy as np

Point = namedtuple('Point', 'x, y')

# RGB colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 127)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREEN =  (0, 255, 0)

BLOCK_SIZE = 20
SPEED = 40 # Update interval in seconds

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4




class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.direction = Direction.RIGHT
        self.snake = []
        self.food = None
        self.score = 0
        self.head = None
        self.batch = pyglet.graphics.Batch()
        self.previous_action = None 
        self.reset()
        #self.clock=pyglet.clock.Clock()
        self.window = pyglet.window.Window(self.w, self.h, "Snake")

        self.snake_rects = []
        self.food_rect = None
        self.score_label = pyglet.text.Label(f"Score: {self.score}",
                                             font_size=12,
                                             x=10, y=self.h - 20,
                                             color=(255, 255, 255, 255),
                                             batch=self.batch)
        self.setup_graphics()
        self.window.push_handlers(self)
        pyglet.clock.schedule_interval(self.update, 1/(SPEED))


        
    def get_game_data(self):
        return {
            "head": self.snake[0],
            "snake": self.snake,
            "food": self.food,
            "direction": self.direction,
        }
    

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w // 2, self.h // 2)
        self.snake = [self.head]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.setup_graphics()

    def setup_graphics(self):
        self.snake_rects = []

        for idx, pt in enumerate(self.snake):
            if idx == 0:  # Head of the snake
                self.snake_rects.append(self.create_rect(pt.x, pt.y, GREEN))
            else:  # Rest of the snake body
                self.snake_rects.append(self.create_rect(pt.x, pt.y, GREEN))

        # Add the food rectangle
        self.food_rect = self.create_rect(self.food.x, self.food.y, RED)


    def on_draw(self):
        self.window.clear()
        self.batch.draw()


    def create_rect(self, x, y, color):
        return pyglet.shapes.Rectangle(x, y, BLOCK_SIZE, BLOCK_SIZE,
                                       color=color, batch=self.batch)

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    """def update(self,action):   
        self.frame_iteration+=1
        self._move(action)
        self.snake.insert(0, self.head)
        reward=0
        game_over=False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            self.snake=[self.head]
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward=10
            self._place_food()
        else:

            self.snake.pop()

        self.update_graphics()
        return reward, game_over, self.score"""
    
    def update(self, action):
        self.frame_iteration += 1
        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False

        # Check for collision with boundaries or self
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            self.snake = [self.head]  # Reset snake
            game_over = True
            reward = -10  # Penalize collision heavily
            return reward, game_over, self.score

        # Reward for getting closer to food
        food_distance_old = self._calculate_food_distance(self.snake[0])
        food_distance_new = self._calculate_food_distance(self.head)

        if self.head == self.food:
            self.score += 1
            reward = 10  # Reward for eating food
            self._place_food()  # Place new food
        else:
            # Penalize for not eating food but reward if moving closer to it
            if food_distance_new < food_distance_old:
                reward = 1  # Small reward for moving closer to the food
            elif food_distance_new > food_distance_old:
                reward = -1  # Small penalty for moving away from the food

            self.snake.pop()  # Remove the tail to simulate movement

        # Penalize repetitive movements
        if action == self.previous_action:
            reward -= 0.1  # Small penalty for repeating the same action
        self.previous_action = action  # Store the action for comparison in the next step

        self.update_graphics()
        return reward, game_over, self.score

    def _calculate_food_distance(self, head):
        """ Calculate the Manhattan distance between the snake's head and the food. """
        return abs(self.food.x - head.x) + abs(self.food.y - head.y)


    def update_graphics(self):
        #for rect in self.snake_rects:
           # rect.delete()
        self.snake_rects = []
        for idx, pt in enumerate(self.snake):
            if idx == 0:  # Head of the snake
                self.snake_rects.append(self.create_rect(pt.x, pt.y, GREEN))
            else:  # Rest of the snake body
                self.snake_rects.append(self.create_rect(pt.x, pt.y, BLUE1))

        self.food_rect.delete()
        self.food_rect = self.create_rect(self.food.x, self.food.y, RED)

        self.score_label.text = f"Score: {self.score}"

        """for rect, pt in zip(self.snake_rects, self.snake):
            rect.x = pt.x
            rect.y = pt.y

        self.food_rect.x = self.food.x
        self.food_rect.y = self.food.y
        self.score_label.text = f"Score: {self.score}"""

    def is_collision(self,pt=None):
        if pt is None:
            pt = self.head
        # Hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # Hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _move(self,action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir
        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
    
if __name__ == "__main__":
    game = SnakeGameAI()
    pyglet.app.run()
