# Snake Game with Q-Learning Automation 🐍🤖

This project is an enhanced version of the classic Snake game, now automated using a **Reinforcement Learning** model known as **Q-Learning**. The program trains an agent to play the game autonomously, continuously improving its performance through experience.

---

## Features

- **Classic Snake Gameplay**: The nostalgic game, now with AI.
- **Q-Learning Agent**: The snake learns from its actions and optimizes its strategy.
- **Performance Graph**: Visualizes the improvement of the AI by plotting average rewards over time.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/APEXPRE123207/Snake_RL_QLearning.git
   cd Snake_RL_QLearning
2. pip install -r requirements.txt


##Usage
To run the program, execute the main.py file:
python main.py

##How It Works
Training: The AI uses Q-Learning to understand the game environment.
Improvement Tracking: A graph is generated to show the snake’s learning progress, displaying the average rewards over episodes.
Graph Visualization
The program dynamically generates a graph that demonstrates the improvement in the snake’s average score as training progresses. This provides insight into the learning process.

File Structure
main.py: Entry point to run the game and AI training.
model.py: Core implementation of the Q-Learning algorithm.
snake.py: Contains the game logic.
plotter.py: Handles graph generation for improvement tracking.

##Future Improvements
Add support for different board sizes.
Explore other reinforcement learning models like Deep Q-Learning.
Implement additional metrics for training evaluation.
Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

License
This project is licensed under the Apache License.


