'''
@author: mroch
'''

# Game representation and mechanics
import checkerboard

# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.  Big sister is watching you :-)

# Python cand load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
import imp
import sys
from statistics import mean
import timer
major = sys.version_info[0]
minor = sys.version_info[1]
modpath = "__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
tonto = imp.load_compiled("tonto", modpath)


# human - human player, prompts for input    
import human
import ai
import minimax

import boardlibrary # might be useful for debugging

from timer import Timer
        

def Game(red=ai.Strategy, black=tonto.Strategy,
         maxplies=10, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 
    """

    # Don't forget to create instances of your strategy,
    # e.g. black('b', checkerboard.CheckerBoard, maxplies)

    #* set inital checker board
    if init == None: init = checkerboard.CheckerBoard()

    #* create instances of strategies
    black = black('b', checkerboard.CheckerBoard, maxplies)
    red = red('r',checkerboard.CheckerBoard, maxplies)

    print("Welcome to the wonderous world of checkers!")
    gameTime = Timer()

    done = False
    move = 1
    rMoveTimeList = []
    bMoveTimeList = []

    while(not done):
        #* Check for winner
        if gameOver(init, rMoveTimeList, bMoveTimeList): break

        #* R's Turn
        if verbose:
            print("\nR Turn:")
            print(init)
        moveTime = Timer()
        init, action = red.play(board=init)         #make move
        rMoveTimeList.append(moveTime.elapsed_s())  # create a list of move times
        move += 1
        if verbose:
            print("move",move,"by r:",init.get_action_str(action), " Result:")
            print(init)
            print("Time - move:", round(rMoveTimeList[-1],2),"s, game:", round(gameTime.elapsed_min(),2),"min")

        #* Check for winner
        if gameOver(init, rMoveTimeList, bMoveTimeList): break

        #* B's Turn
        if verbose:
            print("\nB Turn:")
            print(init)
        moveTime = Timer()
        init, action = black.play(board=init)       #make move
        bMoveTimeList.append(moveTime.elapsed_s())  #add move time to list
        move += 1
        if verbose:
            print("move",move,"by b:", init.get_action_str(action), " Result:")
            print(init)
            print("Time - move:", round(bMoveTimeList[-1], 2), "s, game:", round(gameTime.elapsed_min(), 2), "min")

def gameOver(board, rmoveTimes, bmoveTimes):
    done, winner = board.is_terminal()
    if done:
        #game over
        print("\nFinal Board")
        print(board)
        if winner == None:
            print("It's a draw!")
        else:
            print(winner, "is the winner!")
        print("r Average move time:", mean(rmoveTimes), "seconds")
        print("b Average move time:", mean(bmoveTimes), "seconds")
        return True
    return False #game not over


    
            
if __name__ == "__main__":
    #Game(init=boardlibrary.boards["multihop"])
    #Game(init=boardlibrary.boards["StrategyTest1"])
    #Game(init=boardlibrary.boards["EndGame1"], firstmove = 1)
    Game()
        
        
        


        
                    
            
        

    
    
