'''
Created on Dec 27, 2016

@author: JR
'''

import random


#Needed for the minimax algorithm to store move positions and scores. 
class Move(object):
    def __init__(self, score , pos_tup = None ):
        self.score = score
        self.pos = pos_tup
        

class AI(object):
    '''
    The computer player for tic tac toe,
    will house implementations of minimax and minimax with alpha-beta pruning optimization. 
    '''

    ''' parameter will include mode. which will accept slow or fast. Slow will use bare minimax implementation. Fast will use minimax with ab. 
        allows for future implementation of difficulty modes easy, medium, hard...
    '''
    def __init__(self, mode):
        self.mode = mode
        self.move_count = 0
        self.first_moves = [(0,0),(0,2),(1,1),(2,0),(2,2)]
        
    
    def get_move(self , board):
        self.move_count += 1
        if self.mode == "slow":
            return self.minimax('computer',0, board)
        else:
            if self.move_count == 1:
                return self.minimax_with_ab('computer', -10000, 10000, 0, True , board)
            else:
                return self.minimax_with_ab('computer', -10000, 10000, 0, False , board)
    
    #Updates the list representation of the board. Pass it an x,y position tuple and a string to indicate which marker to use input: 'human'->x , 'computer'->o , 'anythingelse'->None(Used in minimax algorithm)       
    def update_board(self,pos_tup , player, board):
        board_mark = None
        if player == "human":
            board_mark = 'x'
        if player == "computer":
            board_mark = 'o'
        board[pos_tup[0]][pos_tup[1]] = board_mark
            
        
    
    
    #return a list of available moves --> list of position tuples
    def get_available_moves(self,board):
        BOARDHEIGHT = len(board)
        BOARDWIDTH = len(board[0])
        moves = []
        for row in range(BOARDHEIGHT):
            for col in range(BOARDWIDTH):
                if board[row][col] is None:
                    pos_tup = (row , col)
                    moves.append(pos_tup)
        return moves
    
    
    
        #Returns True if the board is full                
    def board_full(self, board):
        BOARDHEIGHT = len(board)
        BOARDWIDTH = len(board[0])
        for row in range(BOARDHEIGHT):
            for col in range(BOARDWIDTH):
                if board[row][col] is None:
                    return False
        return True

    #minimax ai algorithm to determine computer move. 
    def minimax(self, player, depth, board):
        if self.is_winner('human', board):
            return Move(-20 + depth)
        if self.is_winner('computer',board):
            return Move(20 - depth)
        if self.board_full(board):
            return Move(0)
        
        moves = self.get_available_moves(board)
        scores = []
        
        nextplayer = 'human' if player == 'computer' else 'computer'
        
        for move in moves:
            self.update_board(move, player , board)
            mv = Move(self.minimax(nextplayer, depth + 1, board).score, move)
            scores.append(mv)
            self.update_board(move , 'remove', board)
            
        moves = []
        #Want largest number    
        if player == 'computer':
            max = -1000
            for score in scores:
                max = score.score if score.score > max else max
                
            for score in scores:
                if score.score == max:
                    moves.append(score)
            return random.choice(moves)
        else:
            min = 1000
            for score in scores:
                min = score.score if score.score < min else min
                
            for score in scores:
                if score.score == min:
                    moves.append(score)
            return random.choice(moves)
        
    #input a string of the player either 'human' or 'computer' return true if board is in a winning state for that player.
    #could rewrite is_winner to output a char o if any o tokens get 3 in a row, x if x does and some random char if none do. would reduce number of times i need to call. 
    def is_winner(self, player , board):
        mark = 'x' if player == 'human' else 'o'
        count = 0
        count2 = 0
        diag1 = 0
        diag2 = 0
        BOARDHEIGHT = len(board)
        BOARDWIDTH = len(board[0])
        
        #check all possible ways to win for player marker
        for col in range(BOARDWIDTH):
            for row in range(BOARDHEIGHT):
                if board[col][row] == mark:
                    count += 1
                if board[row][col] == mark:
                    count2 += 1
                    
                diag1 = diag1 +  1 if (row == col) and (board[row][col] == mark) else diag1
                diag2 = diag2 + 1 if (row + col == 2) and (board[row][col] == mark) else diag2
            
            if (count == 3 or count2 == 3 or diag1 == 3 or diag2 == 3):
                return True 
            count = 0
            count2 = 0
        
        
        return False
                
    
        
        
    #minimax ai algorithm with alpha beta pruning optimization to determine computer move. 
    def minimax_with_ab(self, player , alpha , beta , depth , first,board):
        if self.is_winner('human',board):
            return Move(-20 + depth)
        if self.is_winner('computer',board):
            return Move(20 - depth)
        if self.board_full(board):
            return Move(0)
        
        moves = self.get_available_moves(board)
        if first:
            move = random.choice(self.first_moves)
            mv = Move(0, move)
            return mv
        
        moves_with_scores = []
        good_moves = []
        
        nextplayer = 'human' if player == 'computer' else 'computer'
        current_best_mv = None
        
        
        for move in moves:
            if player == 'computer':
                    self.update_board(move, player,board)
                    mv = Move((self.minimax_with_ab(nextplayer, alpha, beta,depth+1,first,board).score), move)
                    moves_with_scores.append(mv)
                    if mv.score > alpha:
                        current_best_mv = mv
                        alpha = mv.score
    #                 
                   
                    
            elif player == 'human':
                    self.update_board(move, player,board)
                    mv = Move(self.minimax_with_ab(nextplayer, alpha, beta,depth+1,first,board).score, move)
                    moves_with_scores.append(mv)
                    if mv.score < beta:
                        beta = mv.score
                        current_best_mv = mv
    #                 
    
            self.update_board(move , 'remove',board)
            #prune if alpha >= beta
            if alpha >= beta:
                #print("pruning")
                break
            
        if current_best_mv == None:
            return mv
            
        for move in moves_with_scores:
            if move.score == current_best_mv.score:
                good_moves.append(move)
                    
        
        return random.choice(good_moves)
        