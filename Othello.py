import random
import gym
from gym import spaces
from gym.utils import seeding

step=[-9,-8,-7,-1,1,7,8,9]#8个方向

# 判断是否越界 over(位置)
def over(dir,pos):
  if pos<0 or pos>=64:
    return True
  if pos%8==0 and (dir==4 or dir==7 or dir==2):
    return True
  if pos%8==7 and (dir==3 or dir==0 or dir==5):
    return True
  return False

# 寻找所有能下子的位置 返回pos的list judge(状态，棋子种类)
def judge(state,flag):
  st=[]
  for pos in range(0,64):
    if state[pos]!=0:
      continue
    for i in range(0,8):
      fl = False
      _pos = pos+step[i]
      if over(i, _pos):
        continue
      if state[_pos] != -flag:
        continue

      while True:
        _pos += step[i]
        if over(i, _pos):
          break
        if state[_pos] == 0:
          break
        if state[_pos] == flag:
          fl = True
          break
      if fl:
        st.append(pos)
        break
  return st

# 计算state状态下flag类型棋子的reward
def reward(state,flag):
  s1 = 0  # flag
  s2 = 0  # 非flag
  ss = 0  # 空
  for i in range(0,64):
    if state[i]==flag:
      s1 += 1
    elif state[i]==-flag:
      s2 += 1
    else:
      ss += 1
  return (s1-s2)/64


class OthelloEnv():
    def __init__(self):
      self.state=[0]*64
      self._reset()

    def _step(self, action):
      done=False
      if action[0]==1:
        self.handle(action)
      elif action[0]==-1:
        self.handle(action)
      if len(judge(self.state,1))==0 and len(judge(self.state,-1))==0 :
        done = True
      return self.state, reward(self.state,action[0]), done


    def _reset(self):
      for i in range(64):
        self.state[i] = 0
      self.state[27] = self.state[36] = 1
      self.state[28] = self.state[35] = -1
      return self.state

    # 执行翻转 handle(状态，落子位置，棋子种类)
    def handle(self,action):
      flag=action[0]
      pos=action[1]
      for i in range(0,8):
        _pos=pos+step[i]
        if over(i, _pos):
          continue
        if self.state[_pos]!=-flag :
          continue

        while True:
          _pos += step[i]
          if over(i, _pos) :
            break
          if self.state[_pos] == 0:
            break
          if self.state[_pos] == flag:
            for j in range(pos,_pos,step[i]):
              self.state[j] = flag
              #print(i)
            break
