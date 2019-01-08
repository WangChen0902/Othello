import gym
import matplotlib
import numpy as np
import sys
import random

from collections import defaultdict
import Othello as Env
from Othello import judge


def random_policy(state,flag):
    st=judge(state,flag)
    l=len(st)
    if l==0:
        return [0,0]
    else:
        p=random.randint(0, l-1)
        return [flag,st[p]]

def mc_prediction(policy,env,num_episodes,discount_factor=1.0):
    return_G = defaultdict(float)
    return_N = defaultdict(float)
    Value = defaultdict(float)
    for i_episode in range(num_episodes):
        flag=1
        env._reset()
        state = env.state
        path = []

        while True:
            action = policy(state,flag)
            state, reward, done= env._step(action)
            path.append((action[1],reward,flag))
            # return_G[action[1]] += reward
            if(flag==1):
                return_N[action[1]] += 1.0
            flag = -flag
            if done:
                break
        for pos,i in enumerate(path):
            if (i[2]==1):
                for pos2,e in enumerate(path[pos:]):
                    if (e[2]==1):
                        return_G[i[0]] += e[1]


    for i in range(64):
        if (i != 27 and i != 28 and i != 35 and i != 36):
            Value[i] = return_G[i] * 1.0 / return_N[i]
    #     print(return_N)
    #     print(return_G)
    #     print(return_G.__len__())
    #     print(return_N.__len__())
    return Value

def main():
    value_list=[]
    env = Env.OthelloEnv()
    Value = mc_prediction(random_policy, env, num_episodes=10)
    Value[27]=1
    Value[28]=1
    Value[35]=1
    Value[36]=1
    for i in range(64):
        value_list.append(Value[i])
    # 现有的根据经验得到的矩阵
    # value_list = [10, -9, 8, 4, 4, 8, -9, 10,
    #               -9, -9, -4, -3, -3, -4, -9, -9,
    #               8, -4, 8, 2, 2, 8, -4, 8,
    #               4, 3, 2, 1, 1, 2, 3, 4,
    #               4, 3, 2, 1, 1, 2, 3, 4,
    #               8, -4, 8, 2, 2, 8, -4, 8,
    #               -9, -9, -4, -3, -3, -4, -9, -9,
    #               10, -9, 8, 4, 4, 8, -9, 10]

    # 打印state矩阵
    for i in range(0,8):
        for j in range(0,8):
            print(value_list[8*i+j],end=' ')
            print()
        print()

    # 下棋开始
    def mid_policy(state, flag):
        st = judge(state, flag)
        l = len(st)
        if (l == 0):
            return [0, 0]
        else:
            action = []
            for i in range(l):
                action.append(value_list[i])
            num = max(action)
            p = action.index(num)
            return [flag, st[p]]

    def f(env):
        total = 0
        s = env._reset()
        flag = 1
        action = mid_policy(s, flag)
        d = False
        while not d:
            s, r, d = env._step(action)
            # for i in range(0,8):
            #             #     for j in range(0,8):
            #             #         if(s[8*i+j]==-1):
            #             #             print(s[8*i+j],end=' ')
            #             #         else:
            #             #             print(s[8*i+j],end='  ')
            #             #     print()
            #             # print()
            flag = -flag
            if (flag == 1):
                action = mid_policy(s, flag)
            else:
                action = random_policy(s, flag)
        for i in range(0, 8):
            for j in range(0, 8):
                total += s[8 * i + j]
        # print(total)
        if (total > 0):
            return 1;
        else:
            return 0;

    env = Env.OthelloEnv()
    f(env)
    win = 0
    for i in range(1000):
        win += f(env)
    print(win / 1000)

if __name__ == "__main__":
    main()