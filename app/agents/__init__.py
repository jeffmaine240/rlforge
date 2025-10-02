import numpy as np
import random


class Agent:
    def __init__(self, action_space, state_space, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.action_space = action_space
        self.state_space = state_space
        self.alpha = alpha       # Learning rate
        self.gamma = gamma       # Discount factor
        self.epsilon = epsilon   # Exploration rate

        # Q-table: state → action values
        self.q_table = {}

    def get_state_key(self, state):
        """Convert state into a hashable key."""
        return tuple(np.round(state, decimals=4)) if isinstance(state, (np.ndarray, list)) else state

    def choose_action(self, state):
        """Epsilon-greedy action selection."""
        state_key = self.get_state_key(state)
        if random.random() < self.epsilon or state_key not in self.q_table:
            return self.action_space.sample()
        return int(np.argmax(self.q_table[state_key]))

    def learn(self, state, action, reward, next_state, done):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_space.n)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.action_space.n)

        old_value = self.q_table[state_key][action]
        next_max = np.max(self.q_table[next_state_key])

        # Q-learning update rule
        self.q_table[state_key][action] = old_value + self.alpha * (
            reward + self.gamma * next_max * (not done) - old_value
        )
