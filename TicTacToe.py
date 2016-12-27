'''
Created on Dec 19, 2016

@author: JR
'''
import pygame , random , sys
from pygame.locals import *
from AI import AI



WINDOWHEIGHT = 480
WINDOWWIDTH = 640
PIECESIZE = 100
BOARDWIDTH = 3
BOARDHEIGHT = 3
X_MARGIN = 175
Y_MARGIN = 75
##pos_map maps the inner board positions to the pixel positions they are drawn.(row,column) --> (x pos , y pos)  
pos_map = {(0,0):(175,75) ,  (0,1):(275,75),  (0,2):(375,75),
           (1,0):(175,175) , (1,1):(275,175), (1,2): (375,175),
           (2,0):(175,275) , (2,1):(275,275) ,(2,2):(375,275)}



board = []
turn_flag = None
ai = None

def main():
    global x_img , o_img , screen , turn_flag , first_move,calcs
    calcs = 0
    pygame.init()
    init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Unbeatable Tic-Tac-Toe')
    board_square_img = pygame.image.load("ttt_square.png")
    board_square_img = pygame.transform.smoothscale(board_square_img , (PIECESIZE,PIECESIZE))
    x_img = pygame.image.load('ttt_x.png')
    x_img = pygame.transform.smoothscale(x_img , (PIECESIZE,PIECESIZE))
    o_img = pygame.image.load('ttt_o.png')
    o_img = pygame.transform.smoothscale(o_img, (PIECESIZE, PIECESIZE))
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        x_pos = X_MARGIN
        y_pos = Y_MARGIN
        screen.blit(board_square_img , (X_MARGIN,Y_MARGIN))
        for __ in range(BOARDHEIGHT):
            for _ in range(BOARDWIDTH):
                screen.blit(board_square_img , (x_pos , y_pos))
                x_pos += PIECESIZE
            y_pos += PIECESIZE
            x_pos = X_MARGIN
        draw_board()
        
        if turn_flag == 'human':
            get_human_move()
        else:
#             move = get_computer_move()
            move = ai.get_move(board)
            update_board(move.pos, 'computer')
        
        
#         print('calcs = {}'.format(calcs))
        first_move = False
        if is_winner('human') or is_winner('computer'):
            print('winner')
            clear_board()
        if board_full():
            print('TIE!')
            clear_board()
        turn_flag = 'human' if (turn_flag == 'computer') else 'computer'
        FPSCLOCK.tick(30)
        pygame.display.update()
    
#Initialize board as empty 2d list and randomly chooses whose turn it is. 
def init():
    global ai
    ai = AI('fast')
    for col in range(BOARDWIDTH):
        board.append([])
        for row in range(BOARDHEIGHT):
            board[col].append(None)
            
    turn = ['human' , 'computer']
    global turn_flag, first_move
    first_move = True
    turn_flag = random.choice(turn)
    
def get_human_move():
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN:
                p = event.pos
                if click_on_board(p[0],p[1]):
                    pos_tup = (get_row(p[1]) , get_column(p[0]))
                    if valid_move(pos_tup):
                        update_board(pos_tup, 'human')
                        return
                
        

#Returns True if the board is full                
def board_full():
    for row in range(BOARDHEIGHT):
        for col in range(BOARDWIDTH):
            if board[row][col] is None:
                return False
    return True




#Checks if the current position is a valid move to make. Pass in position tuple return true if it's valid.    
def valid_move(pos_tup):
    return True if board[pos_tup[0]][pos_tup[1]] is None else False

#wipes the board clean
def clear_board():
    global board
    board = []
    init()

#input a string of the player either 'human' or 'computer' return true if board is in a winning state for that player.
#could rewrite is_winner to output a char o if any o tokens get 3 in a row, x if x does and some random char if none do. would reduce number of times i need to call. 
def is_winner(player):
    mark = 'x' if player == 'human' else 'o'
    count = 0
    count2 = 0
    diag1 = 0
    diag2 = 0
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
            
    pass



#Updates the list representation of the board. Pass it an x,y position tuple and a string to indicate which marker to use input: 'human'->x , 'computer'->o , 'anythingelse'->None(Used in minimax algorithm)       
def update_board(pos_tup , player):
    board_mark = None
    if player == "human":
        board_mark = 'x'
    if player == "computer":
        board_mark = 'o'
    board[pos_tup[0]][pos_tup[1]] = board_mark
    
        
#Draws the current board.        
def draw_board():
    for row in range(BOARDHEIGHT):
        for col in range(BOARDWIDTH):
            if board[row][col] is not None:
                img = x_img if board[row][col] == 'x' else o_img
                pos_tuple = (row , col)
                screen.blit(img , pos_map[pos_tuple])
                
    
   
##returns true if the user click is on the tic tac toe board
def click_on_board(x,y):
    if x >= 175 and x <= 475 and y >= 75 and y <= 375:
        return True
    else:
        return False
    

## input x position return the index of the column
def get_column(x):
    if x >=175 and x < 275:
        return 0
    elif x >= 275 and x < 375:
        return 1
    else:
        return 2


##input y position , return index of the row
def get_row(y):
    if y >= 75 and y < 175:
        return 0
    elif y >= 175 and y < 275:
        return 1
    else:
        return 2
    

if __name__ == '__main__':
    main()
    
    
