
import gym
from gym import spaces
from gym.utils import seeding

cards_number = [1,2,3,4,5,6,7,8,9,10,10,10,10]

def clamping(x, y):
    return int((x > y)) - int((x < y))

def picking_card(np_random):
    return np_random.choice(cards_number)

def in_hands(np_random):
    return [picking_card(np_random), picking_card(np_random)]

def total_in_hands(two_cards):
    if Roboace(two_cards):
        return sum(two_cards) + 11
    else:
        return sum(two_cards)

def check_mate(two_cards):
    return sum(two_cards) > 25

def Roboace(two_cards):
    return 1 in two_cards and sum(two_cards) + 10 <= 25

def final_score(two_cards):
    return 0 if check_mate(two_cards) else total_in_hands(two_cards)

def check_nat(two_cards):
    return sorted(two_cards) == [5, 10]


class Environment(gym.Env):
    #action = int(self.action)


    def __init__(self, natural = False):
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Tuple((spaces.Discrete(35),spaces.Discrete(11), spaces.Discrete(2)))

        ## action space - two action : wither draw a card or stop drawing
        ## observation space = tup(sum of values of player, value of card in dealer with face up, Roboace or not ?)
        self.seeding_values()
        self.natural = natural
        self.reset()


    def seeding_values(self, seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):

        # reward = -1 (sum > 25 and episode ends)
        # reward = 0 (for drawing)
        # reward = 1 (for player wins)

        if self.iter:
            print("Player's cards : ", self.player[0], self.player[1])
            self.iter = False

        assert self.action_space.contains(action)
        if action:
            print("PLAYER IS PICKING !!")
            self.player.append(picking_card(self.np_random))
            print("Player picked : ",self.player[-1])
            if check_mate(self.player):
                done = True    #  check this line
                reward = -1

            else:
                done = False
                reward = 0
        else:
            done = False
            print("PLAYER STOPPED TAKING CARDS !!")
            while total_in_hands(self.dealer) < 20:
                print("dealer is picking !!")
                self.dealer.append(picking_card(self.np_random))
                print("Dealer picked : ", self.dealer[-1])
                print("dealer's collection = ", self.dealer)


            reward = clamping(final_score(self.player), final_score(self.dealer))
            if self.natural and check_nat(self.player) and reward == 1:
                reward = 1 # 0, # reward = 1.5
        print("********  REPORT TILL NOW  ********" )
        print("dealer's collection = ", self.dealer)
        print("DEALER'S TOTAL SUM = ", sum(self.dealer))
        print("players collection is ", self.player)
        print("PLAYER'S TOTAL SUM = ", sum(self.player))
        print("*****************************************")

        '''
        ############################   TO DOCUMENT IT IF USED YOUR OWN ENVIRNMENT RUNNER  !!! ###########

        if sum(self.player) > sum(self.dealer):
            print("PLAYER WINS !!")
            print("reward = ", reward)
        elif sum(self.player) < sum(self.dealer):
            print("DEALER WINS !!")
            print("reward = ", reward)
        else:
            print("IT IS DRAW !!")
        
        #########################################################################################
        '''
        return self._get_obs(), reward, done  # , {}

    def _get_obs(self):
        # here, we will get the observation
        return [total_in_hands(self.player), self.dealer[0], Roboace(self.player)]

    def reset(self):
        # reset the information.
        self.dealer = in_hands(self.np_random)
        self.player = in_hands(self.np_random)
        self.iter = True
        while total_in_hands(self.player) < 12:
            self.player.append(picking_card(self.np_random))

        return self._get_obs()

Environment()