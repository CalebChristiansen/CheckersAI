'''
Created on Mar 7, 2020

@author: Caleb & Sharai
'''

import platform  # operating system platform

import checkerboard

import abstractstrategy


class Strategy(abstractstrategy.Strategy):
    "Tonto 2.0"

    def utility(self, board):
        "Return the utility of the specified board"
        numPawns = board.get_pawnsN()
        numKings = board.get_kingsN()

        util =  numPawns[0]-numPawns[1]*2 + numKings[0] * 2-numKings[1] * 3

        #returns the util relative to the maxPlayer
        if (self.maxplayer == 'r'):
            return util
        else:
            return -util

    def play(self, board):
        """"play - Make a move
        Given a board, return (newboard, action) where newboard is
        the result of having applied action to board and action is
        determined via a game tree search (e.g. minimax with alpha-beta
        pruning).
        """

        util, bestAction = self.miniMax(board, self.maxplies, True)

        board = board.move(bestAction)

        return (board, bestAction)

    def miniMax(self, board, depth, maxingPlayer):
        done, winner = board.is_terminal()
        if depth == 0 or done:
            return [self.utility(board), [(0,0), (0,0)]]

        if maxingPlayer:
            maxAction = None
            maxUtil = float("-inf")
            actions = board.get_actions(self.maxplayer)
            for action in actions:
                tempBoard = board.move(action)
                util, prevAction = self.miniMax(tempBoard, depth-1, False)
                if util > maxUtil:
                    maxUtil = util
                    maxAction = action
            return [maxUtil, maxAction]

        else:
            minAction = None
            minUtil = float("inf")
            actions = board.get_actions(self.minplayer)
            for action in actions:
                tempBoard = board.move(action)
                util, prevAction = self.miniMax(tempBoard, depth - 1, True)
                if util < minUtil:
                    minUtil = util
                    minAction = action
            return [minUtil, minAction]