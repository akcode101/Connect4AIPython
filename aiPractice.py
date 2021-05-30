import math

#Thanks to Sebastian Lange for the great explanation of alpha beta pruning!
#https://www.youtube.com/watch?v=l-hh51ncgDI
#Also thanks to https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/ for a great tic-tac-toe sample implementation

#One interesting idea, subtract depth from score for first player; we want white to win as fast as possible, which will hapen if depth is as small as possible
#since less depth means a higher net score. Idea is from geeks for geeks article

#add depth to score for second player; we want black to win as fast as possible, which will happen if depth is as small as possible since less depth means lower score

#only problem with this depth idea is that it may cause us to incorrectly get a draw if for some reason the addition or subtraction causes a score of 0


# another idea, I got from the http://blog.gamesolver.org/, .........................................................................................
# (from a brilliant guy named Pascal Pons who solved Connect 4) , is to use caching to store info about already calculated positions
#another strategy he said was to pick your moves from the middle, as these tend to be the best. He managed to solve it, but I was unable to figure out how to
#efficiently solve the game to the point where the game runs fast. Instead, I created an evaluation function that tries to find as many possible diagonals,
#horizontal token groups, or vertical token groups as possible for the first and second player. Then, I returned the difference of the combo scores
# Additionally, I use a limited depth (not 42!), so the AI runs more quickly. This AI is imperfect.
#
#Another thing he suggested is to try varying the move order to avoid losing moves, which will make the search go faster as we can avoid recursing down a bad
# search tree when there is already a losing move. However, I decided not to i


#What's different in this file: in the minimax function, instead of just returning the score, I also return the move associated with that score, or the most middle
#available column... This avoids having to do potentially unnecessary computation

posInf=float('inf')
negInf=float('-inf')


minimaxParametersToScore=dict()
columnOrderList=[3, 2, 4, 1, 5, 0, 6] #use this column order to traverse columns in middle first, since generally middle columns open up better combos in C-4

##-------
##-------
##-------
##-------
##-------
##XO-----

def printBoard(board):
    for row in board:
        print ('\t'.join([str(position) for position in row]))
        print('\n')
    print('\n')
        


def inBounds(rowPosition, colPosition):
    return (rowPosition>=0 and rowPosition<=5 and colPosition>=0 and colPosition<=6)

def fourScoreUp (board, valueToCheck, rowNumber, columnNumber):
    score=0
    score = score + (1 if (inBounds(rowNumber-1, columnNumber) and board[rowNumber-1][columnNumber]==valueToCheck) else 0)
    if (score==0):
        return score #means that no continuous cluster of tokens, so stop
    score = score + (1 if (inBounds(rowNumber-2, columnNumber) and board[rowNumber-2][columnNumber]==valueToCheck) else 0)
    if (score==1):
        return score
    score = score + (1 if (inBounds(rowNumber-3, columnNumber) and board[rowNumber-3][columnNumber]==valueToCheck) else 0)
    return score

def fourScoreDown (board, valueToCheck, rowNumber, columnNumber):
    score=0
    score = score + (1 if (inBounds(rowNumber+1, columnNumber) and board[rowNumber+1][columnNumber]==valueToCheck) else 0)
    if (score==0):
        return score
    score = score + (1 if (inBounds(rowNumber+2, columnNumber) and board[rowNumber+2][columnNumber]==valueToCheck) else 0)
    if (score==1):
        return score
    score = score + (1 if (inBounds(rowNumber+3, columnNumber) and board[rowNumber+3][columnNumber]==valueToCheck) else 0)
    return score

def fourScoreLeft (board, valueToCheck, rowNumber, columnNumber):
    score=0
    score = score + (1 if (inBounds(rowNumber, columnNumber-1) and board[rowNumber][columnNumber-1]==valueToCheck) else 0)
    if (score==0):
        return score
    score = score + (1 if (inBounds(rowNumber, columnNumber-2) and board[rowNumber][columnNumber-2]==valueToCheck) else 0)
    if (score==1):
        return score
    score = score + (1 if (inBounds(rowNumber, columnNumber-3) and board[rowNumber][columnNumber-3]==valueToCheck) else 0)
    return score

def fourScoreRight (board, valueToCheck, rowNumber, columnNumber):
    score=0
    score = score + (1 if (inBounds(rowNumber, columnNumber+1) and board[rowNumber][columnNumber+1]==valueToCheck) else 0)
    if (score==0):
        return score
    score = score + (1 if (inBounds(rowNumber, columnNumber+2) and board[rowNumber][columnNumber+2]==valueToCheck) else 0)
    if (score==1):
        return score
    score = score + (1 if (inBounds(rowNumber, columnNumber+3) and board[rowNumber][columnNumber+3]==valueToCheck) else 0)
    return score

def fourScoreUpAndLeft (board, valueToCheck, rowNumber, columnNumber):
    score=0
    score = score + (1 if (inBounds(rowNumber-1, columnNumber-1) and board[rowNumber-1][columnNumber-1]==valueToCheck) else 0)
    if (score==0):
        return score
    score = score + (1 if (inBounds(rowNumber-2, columnNumber-2) and board[rowNumber-2][columnNumber-2]==valueToCheck) else 0)
    if (score==1):
        return score
    score = score + (1 if (inBounds(rowNumber-3, columnNumber-3) and board[rowNumber-3][columnNumber-3]==valueToCheck) else 0)
    return score

def fourScoreUpAndRight (board, valueToCheck, rowNumber, columnNumber):
    score=0
    score = score + (1 if (inBounds(rowNumber-1, columnNumber+1) and board[rowNumber-1][columnNumber+1]==valueToCheck) else 0)
    if (score==0):
        return score
    score = score + (1 if (inBounds(rowNumber-2, columnNumber+2) and board[rowNumber-2][columnNumber+2]==valueToCheck) else 0)
    if (score==1):
        return score
    score = score + (1 if (inBounds(rowNumber-3, columnNumber+3) and board[rowNumber-3][columnNumber+3]==valueToCheck) else 0)
    return score

def fourScoreDownAndLeft (board, valueToCheck, rowNumber, columnNumber):
    score=0
    score = score + (1 if (inBounds(rowNumber+1, columnNumber-1) and board[rowNumber+1][columnNumber-1]==valueToCheck) else 0)
    if (score==0):
        return score
    score = score + (1 if (inBounds(rowNumber+2, columnNumber-2) and board[rowNumber+2][columnNumber-2]==valueToCheck) else 0)
    if (score==1):
        return score
    score = score + (1 if (inBounds(rowNumber+3, columnNumber-3) and board[rowNumber+3][columnNumber-3]==valueToCheck) else 0)
    return score

def fourScoreDownAndRight (board, valueToCheck, rowNumber, columnNumber):
    score=0
    score = score + (1 if (inBounds(rowNumber+1, columnNumber+1) and board[rowNumber+1][columnNumber+1]==valueToCheck) else 0)
    if (score==0):
        return score
    score = score + (1 if (inBounds(rowNumber+2, columnNumber+2) and board[rowNumber+2][columnNumber+2]==valueToCheck) else 0)
    if (score==1):
        return score
    score = score + (1 if (inBounds(rowNumber+3, columnNumber+3) and board[rowNumber+3][columnNumber+3]==valueToCheck) else 0)
    return score



#first basic heuristic, multiply effect of multiple clustered tokens all of one color
def boardAnalysis(board, isPlayerOne):
    whiteScoreSum=0
    blackScoreSum=0
    
    for row in range (0, 6):
        for col in range(0, 7):

            
            if (board[row][col]=='X'):
                whiteScoreSum=whiteScoreSum+1
                #check for non-diag combos, white
                whiteScoreSum=whiteScoreSum+fourScoreUp(board, 'X', row, col)
                whiteScoreSum=whiteScoreSum+fourScoreDown(board, 'X', row, col)
                whiteScoreSum=whiteScoreSum+fourScoreLeft(board, 'X', row, col)
                whiteScoreSum=whiteScoreSum+fourScoreRight(board, 'X', row, col)

                #check for diagonal combos, white
                whiteScoreSum=whiteScoreSum+fourScoreUpAndLeft(board, 'X', row, col)
                whiteScoreSum=whiteScoreSum+fourScoreDownAndLeft(board, 'X', row, col)
                whiteScoreSum=whiteScoreSum+fourScoreUpAndRight(board, 'X', row, col)
                whiteScoreSum=whiteScoreSum+fourScoreDownAndRight(board, 'X', row, col)

            if (board[row][col]=='O'):                
                blackScoreSum=blackScoreSum+1
                #check for non-diag combos, black
                blackScoreSum=blackScoreSum+fourScoreUp(board, 'O', row, col)
                blackScoreSum=blackScoreSum+fourScoreDown(board, 'O', row, col)
                blackScoreSum=blackScoreSum+fourScoreLeft(board, 'O', row, col)
                blackScoreSum=blackScoreSum+fourScoreRight(board, 'O', row, col)

                #check for diagonal combos, black
                blackScoreSum=blackScoreSum+fourScoreUpAndLeft(board, 'O', row, col)
                blackScoreSum=blackScoreSum+fourScoreDownAndLeft(board, 'O', row, col)
                blackScoreSum=blackScoreSum+fourScoreUpAndRight(board, 'O', row, col)
                blackScoreSum=blackScoreSum+fourScoreDownAndRight(board, 'O', row, col)
                    

    if isPlayerOne: #means it's player one's turn while playing this position
        return "playing", whiteScoreSum-blackScoreSum

    else: #maybe subtract something from any potential advantage white has of going first, will have to think carefully about this
        return "playing", whiteScoreSum-blackScoreSum

def eval(board, isPlayerOne):

    #checking for vertical wins
    for rowStart in range(3):
        for columnNumber in range(7):
            if (board[rowStart][columnNumber]=='X' and
                board[rowStart+1][columnNumber]=='X' and
                board[rowStart+2][columnNumber]=='X' and
                board[rowStart+3][columnNumber]=='X'):
                    return ("gameOver",posInf)

            if (board[rowStart][columnNumber]=='O' and
                board[rowStart+1][columnNumber]=='O' and
                board[rowStart+2][columnNumber]=='O' and
                board[rowStart+3][columnNumber]=='O'):
                    return ("gameOver",negInf)

    #checking for horizontal wins
    for colStart in range(4):
       for rowNumber in range(6):
           if (board[rowNumber][colStart]=='X' and
               board[rowNumber][colStart+1]=='X' and
               board[rowNumber][colStart+2]=='X' and
               board[rowNumber][colStart+3]=='X'):
                   return ("gameOver", posInf)
           if (board[rowNumber][colStart]=='O' and
               board[rowNumber][colStart+1]=='O' and
               board[rowNumber][colStart+2]=='O' and
               board[rowNumber][colStart+3]=='O'):
                   return ("gameOver",negInf)

    #checking for bottom left to top right diagonal wins
    for rowNumber in range(3,6):
       for colNumber in range(4):
           if (board[rowNumber][colNumber]=='X' and
               board[rowNumber-1][colNumber+1]=='X' and
               board[rowNumber-2][colNumber+2]=='X' and
               board[rowNumber-3][colNumber+3]=='X'):
                   return ("gameOver",posInf)

           if (board[rowNumber][colNumber]=='O' and
               board[rowNumber-1][colNumber+1]=='O' and
               board[rowNumber-2][colNumber+2]=='O' and
               board[rowNumber-3][colNumber+3]=='O'):
                   return ("gameOver",negInf)

    #checking for top left to bottom right diagonal wins
    for rowNumber in range(0, 3):
       for colNumber in range(4):
           if (board[rowNumber][colNumber]=='X' and
               board[rowNumber+1][colNumber+1]=='X' and
               board[rowNumber+2][colNumber+2]=='X' and
               board[rowNumber+3][colNumber+3]=='X'):
                   return ("gameOver",posInf)

           if (board[rowNumber][colNumber]=='O' and
               board[rowNumber+1][colNumber+1]=='O' and
               board[rowNumber+2][colNumber+2]=='O' and
               board[rowNumber+3][colNumber+3]=='O'):
                   return ("gameOver",negInf)

    allColumnsFilled=True
    for i in range(7):
        if board[0][i]=='-':
            allColumnsFilled=False
            break

    if (allColumnsFilled==True):
        return ("gameOver", 0.0) #draw
    else:
        return boardAnalysis(board, isPlayerOne)
        
           
           
               
                   

           
       

#main recursive worker function, evaluates positions
def minimax(board, depthLeft, alpha, beta, isMaximizingPlayer, columnInfo):
    playerMark='X' if isMaximizingPlayer else 'O'
    parList=str(board)+'space'+str(depthLeft)+'space'+str(alpha)+'space'+str(beta)+'space'+str(isMaximizingPlayer)+'space'+str(columnInfo)
    if (parList in minimaxParametersToScore):
        return minimaxParametersToScore[parList]
    status, score= eval(board, isMaximizingPlayer)
    backupCol=3 #3, middle default
    for i in columnOrderList:
        if columnInfo[i]<6:
            backupCol=i
            break
    if depthLeft==0 or status=='gameOver':
            return score, backupCol #backupCol should be between 0 and 6 to be valid, most likely won't be used
    if isMaximizingPlayer:
        maxEval=negInf
        maxCol=-1
        for i in columnOrderList:
            if (columnInfo[i]<6): ##column info counts rows from 0 to 5
                tryRow=columnInfo[i]
                columnInfo[i]=columnInfo[i]+1
                board[5-tryRow][i]=playerMark #We do 5-tryRow because if the available row is 0, in array form it's really 5
                childEval, childCol=minimax(board, depthLeft-1, alpha, beta, not isMaximizingPlayer, columnInfo)
                board[5-tryRow][i]='-'
                columnInfo[i]=columnInfo[i]-1
                if (childEval>maxEval):
                    maxEval=childEval
                    maxCol=i
                alpha=max(alpha, childEval)
                if (beta<=alpha):
                    break
        
        if maxCol==-1:
            for i in columnOrderList:
                if columnInfo[i]<6:
                    maxCol=i
                    break
        minimaxParametersToScore[parList]=(maxEval, maxCol)
        return (maxEval, maxCol)

    else:
        minEval=posInf
        minCol=-1
        for i in columnOrderList:
            if (columnInfo[i]<6):
                tryRow=columnInfo[i]
                columnInfo[i]=columnInfo[i]+1
                board[5-tryRow][i]=playerMark
                childEval, childCol=minimax(board, depthLeft-1, alpha, beta, not isMaximizingPlayer, columnInfo)
                board[5-tryRow][i]='-'
                columnInfo[i]=columnInfo[i]-1
                if (childEval<minEval):
                    minEval=childEval
                    minCol=i
                beta=min(beta, childEval)
                if beta<=alpha:
                    break
        if minCol==-1:
            for i in columnOrderList:
                if columnInfo[i]<6:
                    minCol=i
                    break
        minimaxParametersToScore[parList]=(minEval, minCol)
        return (minEval, minCol)

#what the computer does, here playerMark means the computer is a player
def chooseBestMove(columnInfo, board, isFirst):
    playerMark='X' if isFirst else 'O'
    depth=8
    if (isFirst): #idea is that as a computer, if you're going first, you should look for the maximum minimax value
        evalPosition, evalMove=minimax(board, depth, negInf, posInf, True, columnInfo)
        return evalMove
            
    else:
        evalPosition, evalMove=minimax(board, depth, negInf, posInf, False, columnInfo)
        return evalMove
        

def main():
    sampleBoard= [['-','-','-','-','-','-','-'],
                  ['-','-','-','-','-','-','-'],
                  ['-','-','-','-','-','-','-'],
                  ['X','-','-','O','-','-','-'],
                  ['X','-','-','O','-','-','-'],
                  ['X','-','-','O','-','-','-']]
    sampleColumnInfo=[3, 0, 0, 3, 0, 0, 0]
##    print(minimax(sampleBoard, 10, negInf, posInf, True, sampleColumnInfo))
##    print(chooseBestMove(sampleColumnInfo, sampleBoard, True))

    print("Welcome to Connect 4 vs. the computer!")
    print("When entering moves, enter a column from 0-6, based on the column where you want to go")
    print("0 marks the leftmost column, while 6 marks the rightmost column")

    playerSide=input ("Enter 'first' without single quotes if you want to go first against the computer, otherwise enter 'second': " )
    while (playerSide!='first' and playerSide!='second'):
        playerSide=input ("Enter 'first' without single quotes if you want to go first against the computer, otherwise enter 'second': " )



   


    board= [['-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-'],
            ['-','-','-','-','-','-','-']]

    print("The current empty board will be shown below:\n")
    printBoard(board)
    leastAvailableRowOfEachColumn=[0,0,0,0,0,0,0]
    
    if (playerSide=='first'):
        numberOfMoves=0
        while (True):
            playerColumn=int(input ("Human Player, enter a valid column number: " ))
            while (playerColumn<0 or playerColumn>6 or leastAvailableRowOfEachColumn[playerColumn]>=6):
                playerColumn=int(input ("Human Player, enter a valid column number: "))
            print('\n')
            playerRowOfInterest=leastAvailableRowOfEachColumn[playerColumn]
            board[5-playerRowOfInterest][playerColumn]='X'
            leastAvailableRowOfEachColumn[playerColumn]=leastAvailableRowOfEachColumn[playerColumn]+1
            numberOfMoves=numberOfMoves+1
            gameState, score=eval(board, False) #now, it's player 2's turn
            printBoard(board)
            if (gameState=="gameOver"):
                if score==posInf:
                    print("Player 1, the human wins!")
                    break
                elif score==0.0:
                    print("The game has ended in a draw!")
                    break
            print("Player 2, the computer will now enter the move:\n")
            print(leastAvailableRowOfEachColumn)
            computerMove=chooseBestMove(leastAvailableRowOfEachColumn, board, False)
            availableRow=leastAvailableRowOfEachColumn[computerMove]
            board[5-availableRow][computerMove]='O'
            leastAvailableRowOfEachColumn[computerMove]=leastAvailableRowOfEachColumn[computerMove]+1
            numberOfMoves=numberOfMoves+1
            gameState, score=eval(board, True)
            printBoard(board)
            if (gameState=="gameOver"):
                if score==negInf:
                    print("Player 2, the computer wins!")
                    break
                elif score==0.0:
                    print("The game has ended in a draw!")
                    break
            if (numberOfMoves==42): #only 42 possible moves can be played in this game
                break
    elif playerSide=='second':
        numberOfMoves=0
        while (True):

            print("Player 1, the computer will now enter the move:\n")
            computerMove=chooseBestMove(leastAvailableRowOfEachColumn, board, True) #it's player 1's turn as the computer
            availableRow=leastAvailableRowOfEachColumn[computerMove]
            board[5-availableRow][computerMove]='X'
            leastAvailableRowOfEachColumn[computerMove]=leastAvailableRowOfEachColumn[computerMove]+1
            numberOfMoves=numberOfMoves+1
            gameState, score=eval(board, False)
            printBoard(board)
            if (gameState=="gameOver"):
                if score==posInf:
                    print("Player 1, the computer wins!")
                    break
                elif score==0.0:
                    print("The game has ended in a draw!")
                    break
                
            playerColumn=int(input ("Human Player, enter a valid column number: " ))
            while (playerColumn<0 or playerColumn>6 or leastAvailableRowOfEachColumn[playerColumn]>=6):
                playerColumn=int(input ("Human Player, enter a valid column number: "))
            print('\n')
            playerRowOfInterest=leastAvailableRowOfEachColumn[playerColumn]
            board[5-playerRowOfInterest][playerColumn]='O'
            leastAvailableRowOfEachColumn[playerColumn]=leastAvailableRowOfEachColumn[playerColumn]+1
            numberOfMoves=numberOfMoves+1
            gameState, score=eval(board, True) #now, it's player 1's turn
            printBoard(board)
            if (gameState=="gameOver"):
                if score==negInf:
                    print("Player 2, the human wins!")
                    break
                elif score==0.0:
                    print("The game has ended in a draw!")
                    break
            
            if (numberOfMoves==42): #only 42 possible moves can be played in this game
                break
        
if __name__ == "__main__":
    main()
                
