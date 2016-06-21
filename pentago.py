'''
Chris DeJarlais
TCSS 435
3-14-16
Programming Assignment#2
'''
import sys
import copy
import pyglet

'''this class includes all pentago functionality'''
class PentagoBoard:
    winner = ''
    maxVal = 0
    playerCount = 0
    emptyCount = 0
    openPaths = 0
    temp_count = 0 
    def __init__(self, boardSize):
        self.boardSize = boardSize  
        self.boardState = [['.' for x in range(self.boardSize)] for x in range(self.boardSize)]
    
    def printBoard(self):
        s = '+'
        for column in range(0, self.boardSize + 1):
            if column == (self.boardSize) / 2:
                s += '-+'
            else:
                s += '--'
        s += '-+' 
        print s
        for row in range(0, self.boardSize):
            if row == (self.boardSize) / 2:
                s = '+'
                for column in range(0, self.boardSize + 1):
                    if column == (self.boardSize) / 2:
                        s += '-+'
                    else:
                        s += '--'
                s += '-+'
                print s 
            s = '| '
            for column in range(0, self.boardSize):
                s+= self.boardState[row][column] + ' '
                if column == (self.boardSize - 1) / 2:
                    s+= '| ' 
            s += '|'
            print s
        s = '+'
        for column in range(0, self.boardSize + 1):
            if column == (self.boardSize) / 2:
                s += '-+'
            else: 
                s+= '--'
        s += '-+' 
        print s 
    
    def placePiece(self, block, number, token, board=None):
        if number > 9 or block < 1 or block > 4 or number < 1:
            return -9999 
        column = (number - 1) % 3 
        row = (number - 1) / 3 
        if block % 2 == 0:
            column += 3 
        if block > 2:
            row += 3            
        if board[row][column] == '.':
            board[row][column] = token 
        else:
            print "that state is occupied!"
            return -9999
        return 1 
    def isValidMove(self, block, number, board=None):
        if number > 9:
            return -9999 
        column = (number - 1) % 3 
        row = (number - 1) / 3 
        if block % 2 == 0:
            column += 3 
        if block > 2:
            row += 3            
        if board[row][column] != '.':
            return -9999
        return 1 
    def rotate(self, block, direction, board=None):
        column = 0 
        row = 0 
        if block % 2 == 0:
            column += 3 
        if block > 2:
            row += 3  
        square = []          
        for x in range(column, column + 3):
            for y in range(row, row + 3):
                square.append(board[y][x])
        index = 0
        if direction == 'L' or direction == 'l':    
            for y in range(row + 2, row - 1, -1):
                for x in range(column, column + 3):
                    board[y][x] = square[index]
                    index += 1
        elif direction == 'R' or direction == 'r':
            for y in range(row, row + 3):
                for x in range(column + 2, column - 1 , -1):
                    board[y][x] = square[index]
                    index += 1
    '''this calculates the utility of a pentago state. The utility function was chosen
    to be the number of contiguous 5 sequences available to the maximizing player minus 
    the number of contiguous 5 move sequences available to the minimizing player.''' 
    def utilityCalculator(self, board=None):
        #scan the rows for a winner
        self.openPaths = 0
        player = ""
        #print 'rows done'
        #scan columns for a winner
        player += self.scanRows(True, board)
        player += self.scanColumns(True, board)
        #print 'columns done'
        player += self.scanDiagonalIncreasing(4,0,True, board)
        player += self.scanDiagonalIncreasing(5,0,True, board)
        player += self.scanDiagonalIncreasing(5,1,True, board)
        #print 'diagonal increasing done'
        player += self.scanDiagonalDecreasing(0,0,True, board)
        player += self.scanDiagonalDecreasing(0,1,True, board)
        player += self.scanDiagonalDecreasing(1,0,True, board) 
        #print 'diagonal decreasing done'
        if player == "w":
            return 99999999
        elif player == "b":
            return -99999999
        elif player == "wb" or player == "bw":
            return 0 
        return self.openPaths
   
    '''this determines the presence of a winning state in the game''' 
    def winningState(self):
        #scan the rows for a winner
        self.scanRows()
        #scan columns for a winner
        self.scanColumns()
        self.scanDiagonalIncreasing(4,0)
        self.scanDiagonalIncreasing(5,0)
        self.scanDiagonalIncreasing(5,1)
        self.scanDiagonalDecreasing(0,0)
        self.scanDiagonalDecreasing(0,1)
        self.scanDiagonalDecreasing(1,0) 
     
    def getSuccessors(self, player, board=None):
        successors = []
        for block in range(1, 5):    
            for number in range(1, 10):
                if self.isValidMove(block, number, board) != -9999:
                    for rot_block in range (1, 5):
                        successors.append((block, number, player,(rot_block, 'l')))
                        successors.append((block, number, player,(rot_block, 'r')))
        return successors 

    def minimax(self, action, board=None):
        return self.maxValue(0, 2, action, -999999, 999999, board)[1]
        
    def maximin(self, action, board=None):
        return self.minValue(0, 2, action, -999999, 999999, board)[1]
        
        #return self.minValue(0, 2, action, -999999, 999999, board)[1]
    
    '''this method is a helper method for calculating the min-value. It implements
    alpha-beta pruning. '''
    def minValue(self, depth, target_depth, action, alpha, beta, board=None):
        if depth == target_depth:
            return (self.utilityCalculator(board), action)
        temp = depth + 1
        value = 9999999 
        for action in self.getSuccessors('b', board):
            self.temp_count += 1 
            temp_board = copy.deepcopy(board);
            self.placePiece(action[0], action[1], action[2], temp_board) 
            self.rotate(action[3][0], action[3][1], temp_board)
            value = min(value, self.maxValue(temp, target_depth, action, alpha, beta, temp_board)[0])
            if value <= alpha:#commenting the next this and the next two lines out will convert this to a standard mini-max function, without a
                return value, action
            beta = min(beta, value)
        return value, action 
    
    '''this is a helper method for calculating the max-value. It implements alpha-beta pruning. '''
    def maxValue(self, depth, target_depth, action, alpha, beta, board=None):
        if depth == target_depth:
            return (self.utilityCalculator(board), action)
        temp = depth + 1
        value = -9999999 
        for action in self.getSuccessors('w', board):
            self.temp_count += 1 
            temp_board = copy.deepcopy(board)
            self.placePiece(action[0], action[1], action[2], temp_board) 
            self.rotate(action[3][0], action[3][1], temp_board)
            value = max(value, self.minValue(temp, target_depth, action, alpha, beta, temp_board)[0])
            if value >= beta:#converting this line and the next two lines out will convert this to a standard minimax algorithm
                return value, action
            alpha = max(alpha, value)
        return value, action 
    
    def scanRows(self, utility=False, board=None):
        for y in range(0, self.boardSize):
            player = ''
            self.playerCount = 0
            self.emptyCount = 0
            if utility == True:
                player = ('', y, 0)
            for x in range(0, self.boardSize):
                if utility == False:
                    player = self.winningStateHelper(y, x, player)
                else:
                    player = self.utilityHelper(y, x, player, board)
                    if self.playerCount == 5:
                        return player[0]
                    if player[0] == 'void state':
                        break
                    fringe = (board[y][0] == player[0]) ^ (board[y][self.boardSize - 1] == player[0]) 
                    if fringe and self.playerCount == 1:  
                        player = (player[0], True)
            if utility == True:
                self.emptyCount += self.playerCount
                if self.emptyCount >= self.boardSize - 1:
                    if player[0] != '':
                        if player[1] == False and self.emptyCount == self.boardSize: 
                            self.pathAddition(player, 2)
                        else:
                            self.pathAddition(player, 1) 
            #print 'total number of empty rows', self.emptyCount
        return "" 
    def scanColumns(self, utility=False, board=None):
        for x in range(0, self.boardSize):
            player = ''
            self.playerCount = 0
            self.emptyCount = 0
            if utility == True:
                player = ('', 0, x)
            for y in range(0, self.boardSize):
                if utility == False:
                    player = self.winningStateHelper(y, x, player)
                else:
                    player = self.utilityHelper(y, x, player, board)
                    if self.playerCount == 5:
                        return player[0] 
                    
                    if player[0] == 'void state':
                        break
                    fringe = (board[0][x] == player[0]) ^ (board[self.boardSize - 1][x] == player[0]) 
                    #boolean to indicate the player is in either of outer edges, but not both
                    if fringe and self.playerCount == 1:#if only one occurence of player, and in fringe multiple sequences present 
                        player = (player[0], True)
            self.emptyCount += self.playerCount
            if utility == True:
                if self.emptyCount >= self.boardSize - 1:
                    #self.openPaths += 1  
                    if player[0] != '':
                        if player[1] == False and self.emptyCount == self.boardSize:
                            self.pathAddition(player, 2)
                        else:
                            self.pathAddition(player, 1)
        return ""
    def pathAddition(self, player, cost):
        if player[0] == 'w':
            self.openPaths += cost
            #print 'adding cost ', cost
        else:
            self.openPaths -= cost
            #print 'subtracting cost', cost 
        
             
    def scanDiagonalIncreasing(self, startRow, startColumn, utility=False, board=None):
        self.playerCount = 0
        player = ''
        self.emptyCount = 0 
        if utility == True:
            player = ('', startRow, startColumn)
        for row in range(startRow, startColumn - 1, -1):
            column = startColumn + (startRow - row)
            if utility == False:
                player = self.winningStateHelper(row, column, player) 
            else:
                player = self.utilityHelper(row, column, player, board)
                if self.playerCount == 5:
                    return player[0]
                if player[0] == 'void state':
                    break
                fringe = (board[self.boardSize - 1][0] == player[0]) ^ (board[0][self.boardSize - 1] == player[0]) 
                if fringe and self.playerCount == 1:#if only one occurence of player, and in fringe, multiple sequences present 
                    player = (player[0], True)
                
        if utility == True:
            self.emptyCount += self.playerCount            
            if self.emptyCount >= self.boardSize - 1:
                if player[0] != '':
                    if player[1] == False and self.emptyCount == self.boardSize:
                        self.pathAddition(player, 2) 
                    else:
                        self.pathAddition(player, 1)
        return "" 
    def scanDiagonalDecreasing(self, startRow, startColumn, utility=False, board=None):
        self.playerCount = 0
        player = ''
        self.emptyCount = 0  
        if utility == True:
            player = ('', startRow, startColumn)
        for row in range(startRow, (self.boardSize - startColumn)):
            column = startColumn + (row - startRow)
            if utility == False:
                player = self.winningStateHelper(row, column, player) 
            else:
                player = self.utilityHelper(row, column, player, board)
                if self.playerCount == 5:
                    return player[0] 
                if player[0] == 'void state':
                    #print 'void state'
                    break
                fringe = (board[0][0] == player[0]) ^ (board[self.boardSize - 1][self.boardSize - 1] == player[0])
                if fringe and self.playerCount == 1:    
                    player = (player[0], True) 
        if utility == True:
            self.emptyCount += self.playerCount 
            if self.emptyCount >= self.boardSize - 1:
                if player[0] != '':
                    if player[1] == False and self.emptyCount == self.boardSize:
                        self.pathAddition(player, 2) 
                    else:
                        self.pathAddition(player, 1)
        return ""
    def winningStateHelper(self, row, column, player):
        if self.boardState[row][column] == 'w' or self.boardState[row][column] == 'b':
            if self.boardState[row][column] == player:
                self.playerCount += 1
                if self.playerCount == 5:
                    if self.winner != '' and self.winner != player:
                        print "Tie between the players!"
                    self.winner += player
                if self.playerCount > self.maxVal:
                    self.maxVal = self.playerCount 
            else:
                self.playerCount = 1
                player = self.boardState[row][column]
        else:
            self.playerCount = 0
            player = ''
        return player
    
    def utilityHelper(self, row, column, player, board=None):
        if board[row][column] == '.':
            self.emptyCount += 1
        else:
            if player[0] != '' and board[row][column] != player[0]:  
                #print 'the value of tempCount', self.tempCount
                if self.emptyCount + self.playerCount == self.boardSize - 1:#one complete sequence 
                    if self.playerCount > 1 or player[1] == False:
                        #if at the end, and you encounter a player at the opposite end, this implies a stalemate, not utility benefit
                        self.pathAddition(player[0], 1)
                    self.emptyCount = 0
                self.playerCount = 1
                if player[1] == False:
                    #if the first was not on the fringe this state cannot be won
                    return ('void state', False)
            else:
                self.playerCount += 1
            player = (board[row][column], False)
        return player
                      
def main():
    #window = pyglet.window.Window(700,700)
    
    #image = pyglet.sprite.Sprite('ds3235.gif')
    #sprite = pyglet.sprite.Sprite(animation,x=600,y=600)
    #@window.event
    f = open("output.txt", "w+")
    myPentago = PentagoBoard(6)
    print "welcome to the game of Pentago!"
    name = raw_input("what is your name?")
    player = raw_input("well %s, which player would you like to be? " % name)
    player = int(player)
    str = "player %d name is %s\n" % (player, name)
    if player == 2:
        print "okay, I'll start..."
    else:
        print "go ahead.."
    str_2 = "computer is player %d\n" % (3 - player)
    f.write(str)
    f.write(str_2)
    f.write("player 1 is token white\n")
    f.write("player 2 is token black\n")
    block = 0
    pos = 0
    token = ''
    square = 0
    rot = 'z' 
    while True:
        #print "player %d's turn" % player
        if player == 2:
            token = 'b'
            temp = copy.deepcopy(myPentago.boardState)
            myPentago.temp_count = 0 
            temp = myPentago.minimax((block, pos,(square, rot)), temp)
            #print "the new value of count is %d" % myPentago.temp_count 
            str_move = "%d/%d %d%c\n" %(temp[0],temp[1],temp[3][0],temp[3][1])
            f.write(str_move) 
            myPentago.placePiece(temp[0], temp[1], temp[2], myPentago.boardState) 
            myPentago.winningState()  
            if myPentago.winner != '':    
                break 
            myPentago.rotate(temp[3][0], temp[3][1], myPentago.boardState)
            myPentago.winningState()  
            if myPentago.winner != '':    
                break 
            myPentago.printBoard()  
            move = raw_input("your move: ")
            str_move = move + "\n"
            f.write(str_move)
            moveAndRot =  move.split()
            move = moveAndRot[0].split('/') 
            block = int(move[0])
            pos = int(move[1]) 
            square = int(moveAndRot[1][0])
            rot = moveAndRot[1][1]
            myPentago.placePiece(block, pos, token, myPentago.boardState)
            myPentago.winningState()  
            if myPentago.winner != '':    
                break 
            myPentago.rotate(square, rot, myPentago.boardState)
            myPentago.winningState()  
            if myPentago.winner != '':    
                break 
            for y in range (0, myPentago.boardSize):
                str = ""
                for x in range(0, myPentago.boardSize): 
                    str += myPentago.boardState[y][x]
                str += "\n"    
                f.write(str) 
            myPentago.printBoard()  
        else:
            token = 'w'
            move = raw_input("your move: ")
            str_move = move + "\n"
            f.write(str_move)
            moveAndRot =  move.split()
            move = moveAndRot[0].split('/') 
            block = int(move[0])
            pos = int(move[1]) 
            square = int(moveAndRot[1][0])
            rot = moveAndRot[1][1]
            myPentago.placePiece(block, pos, token, myPentago.boardState)
            myPentago.winningState() 
            if myPentago.winner != '':
                break
            myPentago.rotate(square, rot, myPentago.boardState)
            myPentago.winningState() 
            if myPentago.winner != '':
                break
            myPentago.printBoard()  
            temp = copy.deepcopy(myPentago.boardState)
            myPentago.temp_count = 0
            temp = myPentago.maximin((block, pos,(square, rot)), temp)
            #print "the new value of count is %d" % myPentago.temp_count
            str_move = "%d/%d %d%c\n" % (temp[0],temp[1],temp[3][0],temp[3][1]) 
            f.write(str_move)
            myPentago.placePiece(temp[0], temp[1], temp[2], myPentago.boardState) 
            myPentago.winningState() 
            if myPentago.winner != '':
                break
            myPentago.rotate(temp[3][0], temp[3][1], myPentago.boardState)
            myPentago.printBoard()
            myPentago.winningState() 
            if myPentago.winner != '':
                break
        #myPentago.utilityCalculator()
        #print 'total number of open paths ', myPentago.openPaths
            for y in range (0, myPentago.boardSize):
                str = ""
                for x in range(0, myPentago.boardSize): 
                    str += myPentago.boardState[y][x]
                str += "\n"    
                f.write(str) 
    print "game won by", myPentago.winner 
    myPentago.printBoard() 

main()
'''@window.event
def on_draw():
    window.clear()'''
    
