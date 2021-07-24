### Next attempt will be to buid an RL based algorithm based on Q-learning may be or any another
### after looking at other aspects..

import RL_week_1_solutions
import random

print("\n")

env = RL_week_1_solutions.Environment()
for i in range(5):   ## Initialising the epochs
    ## Each epoch stop when we have a Roboace.
    print("WE ARE IN EPOCH = ", i+1)
    print("\n")
    env.reset()
    done = True
    score = 0

    while done:
        action = random.choice([0,1])
        observ, reward, done_env = env.step(action)

        print("rewarding = ",reward)
        if reward == -1 or reward == 1:
            done = False
        else:
            done = True
        score += reward
    print("***************************************************")
    print("Final score of player of this EPOCH is : ", score)
    print("***************************************************")
    print("\n")