import numpy as np
import random

class QAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.99, epsilon=1.0):
        self.state_size = state_size
        self.action_size = action_size
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = {}

    def get_state_key(self, state):
        return tuple(np.round(state, 4))

    def choose_action(self, state):
        key = self.get_state_key(state)
        if key not in self.q_table:
            self.q_table[key] = np.zeros(self.action_size)

        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.action_size - 1)
        return int(np.argmax(self.q_table[key]))

    def learn(self, state, action, reward, next_state, done):
        key = self.get_state_key(state)
        next_key = self.get_state_key(next_state)

        if key not in self.q_table:
            self.q_table[key] = np.zeros(self.action_size)
        if next_key not in self.q_table:
            self.q_table[next_key] = np.zeros(self.action_size)

        best_next = np.max(self.q_table[next_key])
        td_target = reward + self.gamma * best_next * (not done)
        td_error = td_target - self.q_table[key][action]
        self.q_table[key][action] += self.lr * td_error

        if done:
            self.epsilon = max(0.01, self.epsilon * 0.995)
