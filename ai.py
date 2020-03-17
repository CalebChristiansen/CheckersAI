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

        # check for winning moves
        done, winner = board.is_terminal()
        if (done and winner == self.maxplayer):
            return 99999999999999

        if (done and winner == self.minplayer):
            return -99999999999999

        #this function is written with red as maxPlayer (us) it then negates the score at the
        #end if the maxPlayer was actually black.


        #get number of pawns and kings for each player
        numPawnsR, numPawnsB = board.get_pawnsN()
        numKingsR, numKingsB = board.get_kingsN()

        #ourpices - oppoent's pieces
        util =  numPawnsR - numPawnsB*2 + numKingsR*3 - numKingsB*3*2
        util *= 5 #we want to weight this as more important


        #iterate over each piece on the board
        for piece in board:
            #each piece has properties (r, c, piece)
            row = piece[0]
            col = piece[1]
            pieceType = piece[2]

            #HomeRow Evaluation
            # reward for staying in home row
            if pieceType == 'r' and row == 7:
                util += 15
            # punish opponent staying in last row
            if pieceType == 'b' and row == 0:
                util -= 15

            #Closeness to KingMe!
            #red should try to be in row 0
            if pieceType == 'r':
                util += (7 - row)
            #black should be in 7
            if pieceType == 'b':
                util -= row

            ##prefer double corner kingme
            #if pieceType == 'r' and row <= 2 and col <= 3:
            #    util += 20

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

        print(self.maxplayer, "thinking using tonto 2.0 strategy...")
        util, bestAction = self.miniMax(board, self.maxplies, float("-inf"), float("inf"), True) #maxingPlayer = True

        board = board.move(bestAction)

        return (board, bestAction)


    def miniMax(self, board, depth, alpha, beta, maxingPlayer):
        """
        find the best path/action for either the maxplayer (maxingPlayer = True) or minplayer (maxingPlayer = False)
        uses recursion to compute best path
        :param board: the checkerboard to explore
        :param depth: # of turns to explore (default 10)
        :param alpha: lower bound of possible values for utility
        :param beta:  upper bound of possible values for utility
        :param maxingPlayer: Boolean that tracks if utility is being either max-ed or min-ed
        :return: [util, action] a list containing best util and action for a given player
        """

        done = board.is_terminal()[0]           #* [0] is the done element of return [done, winner]
        if depth == 0 or done:
            return [self.utility(board), None]  #* could return [(0,0),(0,0)]

        if maxingPlayer:                        #* maxingPlayer is a boolean
            maxAction = None                    #* maxAction is the best action of a given utility
            maxUtil = float("-inf")
            actions = board.get_actions(self.maxplayer)
            for action in actions:              #* iterates over all possible actions for this board
                tempBoard = board.move(action)
                util, prevAction = self.miniMax(tempBoard, depth-1, alpha, beta, False)
                if util > maxUtil:
                    maxUtil = util
                    maxAction = action          #* New favorite action
                #* alpha beta pruning
                alpha = max(alpha, util)
                if beta <= alpha: break         #* abandon ship!
            return [maxUtil, maxAction]

        else:                                   #* If maxingPlayer is False
            minAction = None
            minUtil = float("inf")
            actions = board.get_actions(self.minplayer)
            for action in actions:
                tempBoard = board.move(action)
                util, prevAction = self.miniMax(tempBoard, depth - 1, alpha, beta, True)
                if util < minUtil:
                    minUtil = util
                    minAction = action
                beta = min(beta, util)
                if beta <= alpha: break         #* abandon ship!
            return [minUtil, minAction]

