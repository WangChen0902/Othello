#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
from chessboard import ChessBoard
import Othello as Env
import random
import test
import Value_based

WIDTH = 1000
HEIGHT = 1000
MARGIN = 105
GRID = (WIDTH - 2 * MARGIN) / 8
PIECE = 80
EMPTY = 0
BLACK = 1
WHITE = -1

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QPainter
from PyQt5.QtMultimedia import QSound


# ----------------------------------------------------------------------
# 定义线程类执行AI的算法
# ----------------------------------------------------------------------
class AI(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal()

    # 构造函数里增加形参
    def __init__(self, board, parent=None):
        super(AI, self).__init__(parent)
        self.board = board

    # # 重写 run() 函数
    # def run(self):
    #     self.ai = searcher()
    #     self.ai.board = self.board
    #     score, x, y = self.ai.search(2, 2)
    #     self.finishSignal.emit(x, y)


# ----------------------------------------------------------------------
# 重新定义Label类
# ----------------------------------------------------------------------
class LaBel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self, e):
        e.ignore()


class GoBang(QWidget):
    def __init__(self):
        super().__init__()
        self.env = Env.OthelloEnv()
        self.initUI()
        self.i = 0
        self.Q = test.Q

    def initUI(self):

        self.chessboard = ChessBoard()  # 棋盘类

        palette1 = QPalette()  # 设置棋盘背景
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('img/1.jpg')))
        self.setPalette(palette1)
        # self.setStyleSheet("board-image:url(img/chessboard.jpg)")  # 不知道这为什么不行
        self.setCursor(Qt.PointingHandCursor)  # 鼠标变成手指形状

        self.resize(WIDTH, HEIGHT)  # 固定大小 540*540
        self.setMinimumSize(QtCore.QSize(WIDTH, HEIGHT))
        self.setMaximumSize(QtCore.QSize(WIDTH, HEIGHT))

        self.setWindowTitle("黑白棋")  # 窗口名称
        self.setWindowIcon(QIcon('img/black.png'))  # 窗口图标

        # self.lb1 = QLabel('            ', self)
        # self.lb1.move(20, 10)

        self.black = QPixmap('img/black.png')
        self.white = QPixmap('img/white.png')

        self.piece_now = BLACK  # 黑棋先行
        self.my_turn = True  # 玩家先行
        self.step = 0  # 步数
        self.x, self.y = 1000, 1000

        self.mouse_point = LaBel(self)  # 将鼠标图片改为棋子
        self.mouse_point.setScaledContents(True)
        self.mouse_point.setPixmap(self.black)  # 加载黑棋
        self.mouse_point.setGeometry(270, 270, PIECE, PIECE)
        self.pieces = [LaBel(self) for i in range(4096)]  # 新建棋子标签，准备在棋盘上绘制棋子
        for piece in self.pieces:
            piece.setVisible(True)  # 图片可视
            piece.setScaledContents(True)  # 图片大小根据标签大小可变

        self.mouse_point.raise_()  # 鼠标始终在最上层
        self.ai_down = True  # AI已下棋，主要是为了加锁，当值是False的时候说明AI正在思考，这时候玩家鼠标点击失效，要忽略掉 mousePressEvent

        self.draw(3, 3)
        self.draw(3, 4)
        self.draw(4, 4)
        self.draw(4, 3)

        self.setMouseTracking(True)
        self.show()

    def paintEvent(self, event):  # 画出指示箭头
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def mouseMoveEvent(self, e):  # 黑色棋子随鼠标移动
        # self.lb1.setText(str(e.x()) + ' ' + str(e.y()))
        self.mouse_point.move(e.x() - 16, e.y() - 16)

    def print_win(self, d, r, color):
        if d:
            print('finish!')
            if r*color:
                win = 'black'
            else:
                win = 'white'
            QMessageBox.information(self, 'Finish', 'Game over! ' + win + ' win!')

    def mousePressEvent(self, e):  # 玩家下棋
        if e.button() == Qt.LeftButton and self.ai_down == True:
            x, y = e.x(), e.y()  # 鼠标坐标
            i, j = self.coordinate_transform_pixel2map(x, y)  # 对应棋盘坐标
            if not i is None and not j is None:  # 棋子落在棋盘上，排除边缘
                st=[]
                st = Env.judge(self.chessboard.lineboard(),self.piece_now)
                k = i * 8 + j
                if self.chessboard.get_xy_on_logic_state(i, j) == EMPTY and k in st:  # 棋子落在空白处
                    if len(st)!=0:
                        self.draw(i, j)
                        self.env.state = self.chessboard.lineboard()
                        s, r, d = self.env._step([self.piece_now * -1, k])
                        self.drawState(s)
                        print('s:', s)
                        self.print_win(d, r, self.piece_now * -1)

                        self.ai_down = False
                        # AI_action = self.random_policy(s, self.piece_now)
                        # AI_action = Value_based.mid_policy(s, self.piece_now)
                        AI_action = test.make_epsilon_greedy_policy(self.Q, s, self.piece_now, 0.1)
                        if AI_action == [0, 0]:
                            self.piece_now = self.piece_now * -1
                            self.ai_down = True
                        else:
                            s, r, d = self.env._step(AI_action)
                            self.drawState(s)
                            print('s:', s)
                            self.print_win(d, r, self.piece_now)
                            self.piece_now = self.piece_now * -1
                            self.ai_down = True
                    else:
                        self.piece_now = self.piece_now * -1
                        self.ai_down = False
                        # AI_action = self.random_policy(s, self.piece_now)
                        # AI_action = Value_based.mid_policy(s, self.piece_now)
                        AI_action = test.make_epsilon_greedy_policy(self.Q, self.env.state, self.piece_now, 0.1)
                        if AI_action == [0, 0]:
                            self.piece_now = self.piece_now * -1
                            self.ai_down = True
                        else:
                            s, r, d = self.env._step(AI_action)
                            self.drawState(s)
                            print('s:', s)
                            self.print_win(d, r, self.piece_now)
                            self.piece_now = self.piece_now * -1
                            self.ai_down = True

                if self.piece_now == BLACK:
                    self.mouse_point.setPixmap(self.black)
                else:
                    self.mouse_point.setPixmap(self.white)
                    # self.ai_down = False
                    # board = self.chessboard.board()
                    # liner_board = self.chessboard.lineboard()
                    # self.AI = AI(board)  # 新建线程对象，传入棋盘参数
                    # self.AI.finishSignal.connect(self.AI_draw())  # 结束线程，传出参数
                    # self.AI.start()  # run

    def random_policy(self, state, flag):
        st = Env.judge(state, flag)
        l = len(st)
        if l == 0:
            return [0, 0]
        else:
            p = random.randint(0, l - 1)
            return [flag, st[p]]

    def drawState(self, state):
        print(self.i)
        self.i = self.i + 1
        for i in range(0, 8):
            for j in range(0, 8):
                if state[8 * i + j] == -1:
                    self.drawAll(i, j, -1)
                    print(state[8 * i + j], end=" ")
                elif state[8 * i + j] == 1:
                    self.drawAll(i, j, 1)
                    print(state[8 * i + j], end="  ")
                else:
                    print(state[8 * i + j], end="  ")
                    continue
            print()
        print()

    def draw(self, i, j):
        x, y = self.coordinate_transform_map2pixel(i, j)

        if self.piece_now == BLACK:
            self.pieces[self.step].setPixmap(self.black)  # 放置黑色棋子
            self.piece_now = WHITE
            self.chessboard.draw_xy(i, j, BLACK)
        else:
            self.pieces[self.step].setPixmap(self.white)  # 放置白色棋子
            self.piece_now = BLACK
            self.chessboard.draw_xy(i, j, WHITE)

        self.pieces[self.step].setGeometry(x, y, PIECE, PIECE)  # 画出棋子
        self.step += 1  # 步数+1

    def drawAll(self, i, j, color):
        x, y = self.coordinate_transform_map2pixel(i, j)

        if color == BLACK:
            self.pieces[self.step].setPixmap(self.black)  # 放置黑色棋子
            self.chessboard.draw_xy(i, j, BLACK)
        else:
            self.pieces[self.step].setPixmap(self.white)  # 放置白色棋子
            self.chessboard.draw_xy(i, j, WHITE)

        self.pieces[self.step].setGeometry(x, y, PIECE, PIECE)  # 画出棋子
        self.step += 1  # 步数+1

    def drawLines(self, qp):  # 指示AI当前下的棋子
        if self.step != 0:
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(self.x - 5, self.y - 5, self.x + 3, self.y + 3)
            qp.drawLine(self.x + 3, self.y, self.x + 3, self.y + 3)
            qp.drawLine(self.x, self.y + 3, self.x + 3, self.y + 3)

    def coordinate_transform_map2pixel(self, i, j):
        # 从 chessMap 里的逻辑坐标到 UI 上的绘制坐标的转换
        return MARGIN + (j+0.5) * GRID - PIECE / 2, MARGIN + (i+0.5) * GRID - PIECE / 2

    def coordinate_transform_pixel2map(self, x, y):
        # 从 UI 上的绘制坐标到 chessMap 里的逻辑坐标的转换
        i, j = int(math.floor((y - MARGIN) / GRID)), int(math.floor((x - MARGIN) / GRID))
        # 有MAGIN, 排除边缘位置导致 i,j 越界
        if i < 0 or i >= 8 or j < 0 or j >= 8:
            return None, None
        else:
            return i, j



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GoBang()
    sys.exit(app.exec_())

