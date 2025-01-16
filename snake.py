import pyglet
from pyglet.window import key
import random
from enum import Enum
from collections import namedtuple
import numpy as np

BLOCK_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREEN1 = (0, 255, 0)
GREEN2 = (0, 255, 200)
GREEN3= (0, 127, 0)


Direction = Enum('Direction', 'RIGHT LEFT UP DOWN')
Point = namedtuple('Point', 'x, y')


class SnakeGameAI:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.window = pyglet.window.Window(width, height, caption="SnakeGameAI")
        self.reset()

        # Schedule updates
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)
        self.window.push_handlers(self)

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [self.head]
        self.food = None
        self.score = 0
        self.frame_iteration = 0
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        self._move(action)
        self.snake.insert(0, self.head)

        # Check collision
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # Check if food is eaten
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # Update display
        self._update_ui()
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x < 0 or pt.x >= self.width or pt.y < 0 or pt.y >= self.height:
            return True
        if pt in self.snake[1:]:
            return True
        return False

    def _move(self, action):
        # Determine new direction
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clockwise[idx]  # No change
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = clockwise[(idx + 1) % 4]  # Right turn
        else:  # [0, 0, 1]
            new_dir = clockwise[(idx - 1) % 4]  # Left turn

        self.direction = new_dir
        x, y = self.head
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y -= BLOCK_SIZE  
        elif self.direction == Direction.UP:
            y += BLOCK_SIZE

        self.head = Point(x, y)

    def _update_ui(self):
        self.window.clear()

        # Draw the snake body
        for index, segment in enumerate(self.snake):
            if index == 0:  # This is the head of the snake
                self._draw_block(segment, GREEN1) 
                self._draw_inner_block(segment, GREEN2)  
            else:
                self._draw_block(segment, GREEN3)  # Body color
                self._draw_inner_block(segment, GREEN3) 
        # Draw the food
        self._draw_block(self.food, RED)

        # Draw the score
        score_label = pyglet.text.Label(f"Score: {self.score}",
                                        font_size=14,
                                        x=10, y=self.height - 20,
                                        anchor_x='left', anchor_y='center')
        score_label.draw()

    def _draw_block(self, point, color):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', (
            point.x, point.y,
            point.x + BLOCK_SIZE, point.y,
            point.x + BLOCK_SIZE, point.y + BLOCK_SIZE,
            point.x, point.y + BLOCK_SIZE
        )), ('c3B', color * 4))

    def _draw_inner_block(self, point, color):
        offset = 4
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2i', (
            point.x + offset, point.y + offset,
            point.x + BLOCK_SIZE - offset, point.y + offset,
            point.x + BLOCK_SIZE - offset, point.y + BLOCK_SIZE - offset,
            point.x + offset, point.y + BLOCK_SIZE - offset
        )), ('c3B', color * 4))


    def update(self, dt):
        pass  


if __name__ == '__main__':
    game = SnakeGameAI()
    #pyglet.app.run()
