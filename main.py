import pyglet
from snake import SnakeGameAI  
from agent import Agent 
from plotter import plot

class SnakeGameApp:
    def __init__(self):
        self.game = SnakeGameAI()
        self.agent = Agent()
        self.plot_scores = []
        self.plot_mean_scores = []
        self.total_score = 0
        self.record = 0
        self.window = pyglet.window.Window(self.game.width, self.game.height,"SnakeGameAI")
        
        # Schedule the AI logic
        pyglet.clock.schedule_interval(self.update_ai, 1 / 60.0) 
        @self.window.event
        def on_draw():
            self.window.clear()
            self.game._update_ui() 

    def update_ai(self, dt):
        """AI decision and training loop."""
        # Get the current state
        state_old = self.agent.get_state(self.game)

        # Decide the next move
        final_move = self.agent.get_action(state_old)

        # Perform the move
        reward, done, score = self.game.play_step(final_move)
        state_new = self.agent.get_state(self.game)

        # Train the agent
        self.agent.train_short_memory(state_old, final_move, reward, state_new, done)
        self.agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Reset the game and train long-term memory
            self.game.reset()
            self.agent.n_games += 1
            self.agent.train_long_memory()

            if score > self.record:
                self.record = score
                self.agent.model.save()

            print(f"Game {self.agent.n_games}, Score: {score}, Record: {self.record}")

            # Update plotting data
            self.plot_scores.append(score)
            self.total_score += score
            mean_score = self.total_score / self.agent.n_games
            self.plot_mean_scores.append(mean_score)
            plot(self.plot_scores, self.plot_mean_scores)

    def run(self):
        """Run the Pyglet app."""
        pyglet.app.run()


if __name__ == '__main__':
    app = SnakeGameApp()
    app.run()
