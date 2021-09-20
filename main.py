#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import numpy as np
import tetrominos as tet
import matplotlib.pyplot as plt
import time
import pygame
import sys

def framerate(timestep):
    '''
    Parameters
    ----------
    timestep : time when started to count in s

    calculates the framerate of each game loop
    '''
    new_timestep = time.time()
    diff = new_timestep-timestep
    
    return 1/diff


dims = 10           # the pixel size of the atoms
displ_bool = True   # variable for render mode
frame_counter = 0   # frame counter is tied to how often a block drops

#init pygame
pygame.init()
size = [600, 400]   # size of the board, upscaled x2
screen = pygame.display.set_mode((size), pygame.RESIZABLE)
pygame.key.set_repeat(266, 100) # set how long it takes for repeat input
                                # you need to restart the kernel for this for
                                # some reason in spyder

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
    fr = framerate(timestep) # calculate framerate
    timestep = time.time()   # start new timecount for next loopthrough of gameloop
    #print(fr)
    
# =============================================================================
# move down  
# do this with multiprocessing later?
# =============================================================================
    dummy_board = board.board.copy()    #make a copy of the np board where the current piece lives
    dummy_board[board.y:board.y+board.piece.shape[0], board.x:board.x+board.piece.shape[1]] += board.piece  # add the piece to the board  

    #piece speed
    #this will need to be changed for ml agents
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
                board.game_over = True
            elif event.type == pygame.KEYDOWN:
                #print(event.key)
                if event.key == 114: # the r key for render toggle
                    displ_bool = not displ_bool
                elif event.key == 27: #escape key
                    board.game_over = True
                elif event.key == 32: #  space
                    board.rotate()
                elif event.key ==  1073741903: #right key
                    board.move_right()
                elif event.key == 1073741904: #right key
                    board.move_left()
                elif event.key == 1073741905: #down key
                    board.move_down()
                    
# =============================================================================
#   only draw to screen when specified
# =============================================================================
    #make a correct pygame object for the screen from our numpy arrays
    dummy_board = dummy_board[:20*dims,2*dims:12*dims,:] # cut off edges
    dummy_board = board.final_array(dummy_board)         # add score, level, next piece
    
    
    if displ_bool: # only print to screen if render mode is set to true
        board_game = pygame.pixelcopy.make_surface(dummy_board)  # convert from numpy array to pygame object
        flipped = pygame.transform.flip(board_game, True, False) # since indexing is the other way around in pygame
        rotated = pygame.transform.rotate(flipped, 90)           # we need to flip and rotate the board
        
        #scale to the right size and blit to screen
        scaled_win = pygame.transform.scale(rotated, screen.get_size())
        screen.blit(scaled_win, (0,0))
        
        #draw to screen
        pygame.display.update()
        

print(f"your final score is {board.score}")

# quit pygame and close script correctly
pygame.quit()
sys.exit()
