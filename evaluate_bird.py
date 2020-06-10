from flappy import FlappyBird
import numpy as np
import matplotlib.pyplot as plt
from algorithms import q_learning

def evaluate_learning(
        sim,series_size=50, num_series=20, gamma=0.99, alpha=0.7,
        epsilon=0.0001):
    '''
    :param sim: The queuing object
    :param series_size: the size of series
    :param num_series: the number of series
    :return: a result policy
    '''
    # initialise Q values

    #Q = 0*np.ones((sim.num_states,sim.num_actions))
    Q = np.load('save.npy')
    print(Q.shape)
    figrew, axrew = plt.subplots()
    total_reward_seq = [0]
    total_episodes = 0

    for series in range(num_series):
        print("series = %r/%d" % (series,num_series) ) # Print the current stage
        rewardlist=[]
        for episode in range(series_size):
            policy, Q = q_learning(
                sim, gamma=gamma, alpha=alpha, epsilon=epsilon,
                num_episodes=1, initial_Q=Q)
            rewardlist.append(
                sim.score)
            total_episodes += 1
        Q2=Q
        total_reward_seq.append(np.mean(np.array(rewardlist)))

        np.save('save.npy',Q2)
    total_reward_seq = np.array(total_reward_seq)
    axrew.plot(
        np.arange(0, total_episodes+1, series_size),
        total_reward_seq)
    axrew.set_xlabel("episodes")
    axrew.set_ylabel("average score")
    return policy

policy=evaluate_learning(sim=FlappyBird())
plt.title('Average score per series')
plt.tight_layout()
plt.show()
