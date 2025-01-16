from agent import Agent
from snake import SnakeGameAI

def run_with_pretrained_model():
    # Initialize the game and agent
    game = SnakeGameAI()
    agent = Agent()

    # Load the pre-trained model
    agent.load_model("./model/model.pth")

    while True:
        state = agent.get_state(game)
        action = agent.get_action(state)  # Predict action using the model
        reward, done, score = game.update(action)

        if done:
            print(f"Game Over! Score: {score}")
            game.reset()  # Reset the game after it ends

if __name__ == "__main__":
    run_with_pretrained_model()
