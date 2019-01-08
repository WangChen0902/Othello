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


def f(state, action):
    e = Env.OthelloEnv()
    e.state = state
    s, r, d = e._step(action)
    return s, d


env = Env.OthelloEnv()
env._reset()
ss, dd = f(env.state, random_policy(env.state, 1))
print(ss)
print(dd)
