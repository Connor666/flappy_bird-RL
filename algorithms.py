import numpy as np
import copy
import matplotlib.pyplot as plt

def sarsa(
        env, gamma, alpha, epsilon, num_episodes, max_steps=np.inf,
        initial_Q=None):
    """
      Estimates optimal policy by interacting with an environment using
      a td-learning approach

      parameters
      ----------
      env - an environment that can be reset and interacted with via step
          (typically this might be an MDPSimulation object)
      gamma - the geometric discount for calculating returns
      alpha - the learning rate
      epsilon - the epsilon to use with epsilon greedy policies
      num_episodes - number of episode to run
      max_steps (optional) - maximum number of steps per trace (to avoid very
          long episodes)

      returns
      -------
      policy - an estimate for the optimal policy
      Q - a Q-function estimate of the output policy
    """
    num_states = env.num_states
    num_actions = env.num_actions
    if initial_Q is None:
        Q = np.zeros((num_states, num_actions))
    else:
        Q = initial_Q
    policy = get_epsilon_greedy_policy(epsilon, Q, env.absorbing)
    for _ in range(num_episodes):
        # reset state
        s = env.reset()
        # choose initial action
        a = choose_from_policy(policy, s)

        steps = 0
        while not env.is_terminal() and steps < max_steps:
            next_s, r = env.next(a)
            # choose the next action
            next_a = choose_from_policy(policy, s)
            # get td_error (called delta on slides)
            td_error = r + gamma * Q[next_s, next_a] - Q[s, a]
            # update the Q function estimate
            Q[s, a] += alpha * td_error
            # update the policy (only need to do so for current state)
            policy[s, :] = get_epsilon_greedy_policy(
                epsilon, Q[s, :].reshape((1, num_actions)))
            # set next state and action to current state and action
            s = next_s
            a = next_a
            # increment the number of steps
            steps += 1
    # return the policy
    return policy, Q


def q_learning(
        env, gamma, alpha, epsilon, num_episodes, max_steps=np.inf,
        initial_Q=None):
    """
      Estimates optimal policy by interacting with an environment using
      a td-learning approach

      parameters
      ----------
      env - an environment that can be initialised and interacted with
          (typically this might be an MDPSimulation object)
      gamma - the geometric discount for calculating returns
      alpha - the learning rate
      epsilon - the epsilon to use with epsilon greedy policies
      num_episodes - number of episode to run
      max_steps (optional) - maximum number of steps per trace (to avoid very
          long episodes)

      returns
      -------
      policy - an estimate for the optimal policy
      Q - a Q-function estimate of the optimal epsilon-soft policy
    """
    num_states = env.num_states
    num_actions = env.num_actions
    if initial_Q is None:
        Q = np.zeros((num_states, num_actions))
    else:
        Q = initial_Q
    policy = get_epsilon_greedy_policy(epsilon, Q, env.absorbing)
    for _ in range(num_episodes):
        # initialise state
        s = env.reset()
        steps = 0
        done = False
        while not env.is_terminal() and steps < max_steps:
            # choose the action
            a = choose_from_policy(policy, s)
            next_s, r = env.next(a)
            # get td_error (called delta on slides)
            td_error = r + gamma * np.max(Q[next_s, :]) - Q[s, a]
            # update the Q function estimate
            Q[s, a] += alpha * td_error
            # update the policy (only need to do so for current state)
            policy[s, :] = get_epsilon_greedy_policy(
                epsilon, Q[s, :].reshape((1, num_actions)))
            # set next state and action to current state and action
            s = next_s
            # increment the number of steps
            steps += 1
    # return the policy
    return get_greedy_policy(Q, absorbing=env.absorbing), Q


def choose_from_policy(policy, state):
    num_actions = policy.shape[1]
    return np.random.choice(num_actions, p=policy[state, :])


def get_epsilon_greedy_policy(epsilon, Q, absorbing=None):
    """
    Returns an epsilon-greedy policy from a Q-function estimate

    parameters
    ----------
    epsilon - should be 0<epsilon<0.5. This is the variable that controls the
        degree of randomness in the epsilon-greedy policy.
    Q - (num_states x num_actions) matrix of Q-function values
    absorbing (optional) - A vector of booleans, indicating which states are
        absorbing (and hence do not need action decisions). if specified then
        the rows of the output policy will not specify a probability vector

    returns
    -------
    policy - (num_states x num_actions) matrix of state dependent action
        probabilities.
    """
    num_actions = Q.shape[1]
    greedy_policy = get_greedy_policy(Q, absorbing=absorbing)
    policy = (1 - epsilon) * greedy_policy + epsilon * np.ones(Q.shape) / num_actions
    return policy


def get_greedy_policy(Q, absorbing=None):
    """
    Returns the greedy policy from a Q-function estimate

    parameters
    ----------
    Q - (num_states x num_actions) matrix of Q-function values
    absorbing (optional) - A vector of booleans, indicating which states are
        absorbing (and hence do not need action decisions). if specified then
        the rows of the output policy will not specify a probability vector

    returns
    -------
    policy - (num_states x num_actions) matrix of state dependent action
        probabilities. However this will contain just one 1 per row with
        all other values zero. If a vector specifying absorbing states is
        pass in then the corresponding rows will not be a valid probability
        vector
    """
    num_states, num_actions = Q.shape
    dominant_actions = np.argmax(Q, axis=1)
    policy = np.zeros((num_states, num_actions))
    policy[np.arange(num_states), dominant_actions] = 1.
    if not absorbing is None:
        # np.nan means Not-a-number, so the rows for absorbing states are
        # not valid probability vectors
        policy[absorbing, :] = np.nan
    return policy
