import gym
import matplotlib
import numpy as np
import sys
import random

from collections import defaultdict
import Othello as Env
from Othello import judge
# 根据的V表
value_list = [10, -9, 8, 4, 4, 8, -9, 10,
              -9, -9, -4, -3, -3, -4, -9, -9,
              8, -4, 8, 2, 2, 8, -4, 8,
              4, 3, 2, 1, 1, 2, 3, 4,
              4, 3, 2, 1, 1, 2, 3, 4,
              8, -4, 8, 2, 2, 8, -4, 8,
              -9, -9, -4, -3, -3, -4, -9, -9,
              10, -9, 8, 4, 4, 8, -9, 10]
# 根据表选择的策略
def mid_policy(state,flag):
    st = judge(state,flag)
    l=len(st)
    if(l==0):
        return[0,0]
    else:
        action = []
        for i in range(l):
            action.append(value_list[i])
        num = max(action)
        p = action.index(num)
        return [flag,st[p]]
# 随机策略
def random_policy(state,flag):
    st=judge(state,flag)
    l=len(st)
    if l==0:
        return [0,0]
    else:
        p=random.randint(0, l-1)
        return [flag,st[p]]

# 下棋过程
def f(env):
    total=0
    s = env._reset()
    flag=-1
    action = mid_policy(s, flag)
    d=False
    while not d:
        s,r,d = env._step(action)
        for i in range(0,8):
            for j in range(0,8):
                if(s[8*i+j]==-1):
                    print(s[8*i+j],end=' ')
                else:
                    print(s[8*i+j],end='  ')
            print()
        print()
        flag=-flag
        if(flag==-1):
            action = mid_policy(s, flag)
        else:
            action = random_policy(s, flag)
    # 计算输赢
    # for i in range(0,8):
    #     for j in range(0,8):
    #         total+=s[8*i+j]
    # print(total)
    # if(total <  0):
    #     return 1;
    # else:
    #     return 0;

env = Env.OthelloEnv()
# f(env)

