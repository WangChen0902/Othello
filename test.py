import gym
import matplotlib
import numpy as np
import sys
import random

from collections import defaultdict
import Othello as Env
from Othello import judge


def random_policy(state,flag):
    st = judge(state,flag)
    l = len(st)
    if l == 0:
        return [0, 0]
    else:
        p = random.randint(0, l-1)
        return [flag,st[p]]


def make_epsilon_greedy_policy(Q, state, flag, epsilon):
    # print(flag)
    st = judge(state, flag)
    l = len(st)
    if (tuple(state), flag) not in Q.keys():
        q_dict = {}
        for ch in st:
            q_dict[ch] = 0
        Q[(tuple(state), flag)] = q_dict
    if l == 0:
        Q[(tuple(state), flag)] = {0: 0}
        return [0, 0]
    else:
        ran = np.random.randint(0, 100)
        if ran >= epsilon*100:
            action = max(Q[(tuple(state), flag)], key=Q[(tuple(state), flag)].get)
        else:
            action = st[random.randint(0, l-1)]
        return [flag, action]


def f(env, num_episodes, discount_factor=1.0, epsilon=0.1, alpha=0.1):
    Q = {}
    win_time = 0
    for e in range(num_episodes):
        def opp(op_s, op_f):
            op_a = random_policy(op_s, op_f)
            op_n_s, op_r, op_d = env._step(op_a)
            op_f = -op_f
            return op_n_s, op_d, op_f

        if e % 100 == 1:
            print('e:', e)
            print('win_rate:', win_time/e)
        s = env._reset()
        flag = 1
        d = False
        s, d, flag = opp(s, flag)
        a = make_epsilon_greedy_policy(Q, s, flag, epsilon)

        while not d:
            # print(Q)
            t_s = tuple(s)
            op_next_s, r, d = env._step(a)
            flag = -flag
            next_s, d, flag = opp(op_next_s, flag)
            next_a = make_epsilon_greedy_policy(Q, next_s, flag, epsilon)
            t_next_s = tuple(next_s)
            g = r + discount_factor * Q[(t_next_s, flag)][next_a[1]]
            Q[(t_s, flag)][a[1]] = Q[(t_s, flag)][a[1]] + alpha * (g - Q[(t_s, flag)][a[1]])
            s = next_s
            a = next_a

            # for i in range(0,8):
            #     for j in range(0,8):
            #         if s[8*i+j] == -1:
            #             print(s[8*i+j], end=" ")
            #         else:
            #             print(s[8*i+j], end="  ")
            #     print()
            # print()
            # print(Q)
            # print(d)
        if r > 0:
            win_time += 1
        # print()

    return Q, win_time

env = Env.OthelloEnv()
Q, win_time = f(env, num_episodes=5000, epsilon=0.1)
print(len(Q))
# f = open('result2.txt', 'w')
# f.write(str(Q))
# f.close()
# print('wintime:', win_time)
