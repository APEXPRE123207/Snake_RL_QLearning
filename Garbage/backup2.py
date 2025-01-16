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


"""class SnakeGameAI:
    def get_game_data(self):
        return {
            "head": self.snake[0],
            "snake": self.snake,
            "food": self.food,
            "direction": self.direction,
        }
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.direction = Direction.RIGHT
        self.head = Point(self.w // 2, self.h // 2)
        self.snake = [self.head]
        self.score = 0
        self.food = None
        self.frame_iteration = 0
        self.batch = pyglet.graphics.Batch()
        self.reset()
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
        pyglet.clock.schedule_interval(self.update([1, 0, 0]), 1 / SPEED)"""
class SnakeGameAI:
    def get_game_data(self):
        return {
            "head": self.snake[0],
            "snake": self.snake,
            "food": self.food,
            "direction": self.direction,
        }
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.direction = Direction.RIGHT
        self.head = Point(self.w // 2, self.h // 2)
        self.snake = [self.head]
        self.score = 0
        self.food = None
        self.batch = pyglet.graphics.Batch()
        self.frame_iteration = 0
        self.current_action = [1, 0, 0]  # Default to moving straight
        self.reset()

        self.batch = pyglet.graphics.Batch()
        self.window = pyglet.window.Window(self.w, self.h, "Snake")
        self.snake_rects = []
        self.food_rect = None
        self.score_label = pyglet.text.Label(
            f"Score: {self.score}",
            font_size=12,
            x=10, y=self.h - 20,
            color=(255, 255, 255, 255),
            batch=self.batch
        )

        self.setup_graphics()
        self.window.push_handlers(self)

        # Schedule update with a reference to the current action
        pyglet.clock.schedule_interval(self.scheduled_update, 1 / SPEED)

    def set_action(self, action):
        """Update the current action."""
        self.current_action = action

    def scheduled_update(self, dt):
        """Call the update method with the current action."""
        self.update(self.current_action)


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

    def create_rect(self, x, y, color):
        return pyglet.shapes.Rectangle(x, y, BLOCK_SIZE, BLOCK_SIZE,
                                       color=color, batch=self.batch)

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def update(self, action):  # Updated to use action parameter from agent
        #action=[0,0,1]
        #print("Prev: ",action)
        """if action not in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]:
            action = [1, 0, 0]
        #print("After: ",action)"""
        """self.frame_iteration += 1
        self._move(action)  # Move the snake
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 1000 * len(self.snake):
            self.snake = [self.head]
            game_over = True
            reward = -2000
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 200
            self._place_food()
        else:
            self.snake.pop()

        self.update_graphics()
        return reward, game_over, self.score"""

        #print("Action received: ", action)
        self.frame_iteration += 1
        self._move(action)  # Move the snake
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            self.snake = [self.head]
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        self.update_graphics()
        return reward, game_over, self.score


    def update_graphics(self):
        self.snake_rects = []
        for idx, pt in enumerate(self.snake):
            if idx == 0:  # Head of the snake
                self.snake_rects.append(self.create_rect(pt.x, pt.y, GREEN))
            else:  # Rest of the snake body
                self.snake_rects.append(self.create_rect(pt.x, pt.y, BLUE1))

        self.food_rect.delete()
        self.food_rect = self.create_rect(self.food.x, self.food.y, RED)

        self.score_label.text = f"Score: {self.score}"

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # Hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        #print("action:", action)
        #print(self.direction, end=" -> ")
        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            #print("Bye")
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir
        #print(self.direction)

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y += BLOCK_SIZE

        self.head = Point(x, y)
        #print(f"Direction: {self.direction}, Head: {self.head}")

# In the main function:
if __name__ == "__main__":
    game = SnakeGameAI()
    pyglet.app.run()


"""import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 40

class SnakeGameAI:

    def get_game_data(self):
        return {
            "head": self.snake[0],
            "snake": self.snake,
            "food": self.food,
            "direction": self.direction,
        }
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def update(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
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

# In the main function:
if __name__ == "__main__":
    game = SnakeGameAI()
    while True:
        game.update() # move straight
        pygame.time.wait(100)"""
        

