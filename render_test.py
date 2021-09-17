#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import numpy as np
import tetrominos as tet
import time
import pygame
import sys

dims = 10
displ_bool = True 
frame_counter = 0

def framerate(timestep):
    new_timestep = time.time()
    diff = new_timestep-timestep
    
    return 1/diff


#init pygame
pygame.init()
size = [600, 400]
screen = pygame.display.set_mode((size), pygame.RESIZABLE)
pygame.key.set_repeat(266, 100) # set how long it takes for repeat input
                                # you need to restart the kernel for this for
                                # some reason in spyder

#board objects
fontname = pygame.font.get_default_font()
myfont = pygame.font.SysFont("Comic Sans MS", 30)
yellow = (255, 0, 0)



#make board
board = tet.Board(dims)

#start timer
timestep = frametime = time.time()

# =============================================================================
# game loop
# =============================================================================
while not board.game_over:
    
# =============================================================================
#     framerate counter
# =============================================================================
    fr = framerate(timestep)
    timestep = time.time()
    print(fr)
    
# =============================================================================
# move down  
# do this with multiprocessing later?
# =============================================================================
    dummy_board = board.board.copy()
    dummy_board[board.y:board.y+board.piece.shape[0], board.x:board.x+board.piece.shape[1]] += board.piece    

    #piece speed
    if (time.time()-frametime) >= (1/60): #run at 60 fps
        frame_counter += 1
        frametime = time.time()
    
    if frame_counter >= board.fpg:
        frame_counter = 0
        board.move_down()
    
# =============================================================================
#   event handler
# =============================================================================
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                #print(event.key)
                if event.key == 112: # the p key for pause
                    displ_bool = not displ_bool
                elif event.key == 27: #escape key
                    pygame.quit()
                elif event.key == 32: # space
                    board.rotate()
                elif event.key ==  1073741903: #right key
                    board.move_right()
                elif event.key == 1073741904: #right key
                    board.move_left()
                elif event.key == 1073741905:
                    board.move_down()
                    
# =============================================================================
#   only draw to screen when specified
# =============================================================================
   
    #make a correct pygame object for the screen from our numpy arrays
    dummy_board = dummy_board[:20*dims,2*dims:12*dims,:]
    dummy_board = board.final_array(dummy_board)
    #board_game = pygame.pixelcopy.make_surface()
    board_game = pygame.pixelcopy.make_surface(dummy_board)
    flipped = pygame.transform.flip(board_game, True, False)
    rotated = pygame.transform.rotate(flipped, 90)
    
    scaled_win = pygame.transform.scale(rotated, screen.get_size())
    screen.blit(scaled_win, (0,0))
    
    #blit in scores
    score_title = myfont.render("score", 1, yellow)
    screen.blit(score_title, (0,0))
    score = myfont.render(str(board.score), 1, yellow)
    screen.blit(score, (0, 30))
    level_title = myfont.render("level", 1, yellow)
    screen.blit(level_title, (0,60))
    level = myfont.render(str(board.level), 1, yellow)
    screen.blit(level, (0,90))
    
    #blit in next piece
    next_piece = pygame.pixelcopy.make_surface(board.next_piece_display)
    next_piece_flipped = pygame.transform.flip(next_piece, True, False)
    next_piece_rotated = pygame.transform.rotate(next_piece_flipped, 90)
    #screen.blit(next_piece_rotated, (200, 0))

    factor = [screen.get_size()[i]/size[i] for i in range(2)]
    scale_var = [int(8*board.dims*i) for i in factor] # since board size is (600,400) instead of (300,200)
    place = [int((i*(7/9))) for i in screen.get_size()]
    place = [int(screen.get_size()[0]*7/9), int(screen.get_size()[1]*1/9)]
    
    next_piece_scaled = pygame.transform.scale(next_piece_rotated, scale_var)
    screen.blit(next_piece_scaled, (place))
    
    if displ_bool: 
        pygame.display.update()
        

print(f"your final score is {board.score}")
pygame.quit()
        
