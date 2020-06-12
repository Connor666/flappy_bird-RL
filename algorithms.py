import numpy as np

def q_learning(
        env, gamma, alpha, epsilon, num_episodes,Qtable, max_steps=np.inf):
    num_states = env.num_states
    num_actions = env.num_actions
    policy = get_soft_greedy_policy(epsilon, Qtable)
    for _ in range(num_episodes):
        # initialise state
        s = env.reset()
        steps = 0
        done = False
        while not env.is_terminal() and steps < max_steps:
            # choose the action
            a = choose_from_policy(policy, s)
            next_s, r = env.next(a)
            # update the Q function estimate
            Qtable[s, a] += alpha * (r + gamma * np.max(Qtable[next_s, :]) - Qtable[s, a])
            # update the policy (only need to do so for current state)
            policy[s, :] = get_soft_greedy_policy(
                epsilon, Qtable[s, :].reshape(1,num_actions))
            s = next_s
            steps += 1
    # return the policy
    return Qtable


def choose_from_policy(policy, state):
    num_actions = policy.shape[1]
    result= np.random.choice(num_actions, p=policy[state, :])
    return result


def get_soft_greedy_policy(epsilon, Q):
    greedy_policy = get_greedy_policy(Q)
    policy = (1 - epsilon) * greedy_policy + epsilon * np.ones(Q.shape) / Q.shape[1]
    return policy


def get_greedy_policy(Q):
    num_states, num_actions = Q.shape
    policy = np.zeros((num_states, num_actions))
    dominant_actions = np.argmax(Q, axis=1)
    policy[np.arange(num_states), dominant_actions] = 1.
    return policy
