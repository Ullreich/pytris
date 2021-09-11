import numpy as np
import pygame
import time
import concurrent.futures 

# TODO
# run at 60 fps/run uncapped
# use multiprocessing
# fix: tetromino can't fall all the way down due to filler atoms
# https://harddrop.com/wiki/Tetris_(NES,_Nintendo) for specification


def framerate(timestep):
    new_timestep = time.time()
    diff = new_timestep-timestep
    
    return 1/diff

atom_size = 10
frames_per_gridcell = 48
frame_counter = 48
height = 0

displ_bool = True

t_piece = np.load("t_test.npy")
board = np.zeros(shape=(atom_size*20,atom_size*10,3), dtype='int64')

#init pygame
pygame.init()
screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)


#start timer
timestep = frametime = time.time()
while True:
# =============================================================================
#     framerate counter
# =============================================================================
    fr = framerate(timestep)
    timestep = time.time()
    print(fr)
    
# =============================================================================
# move down  
# do this with multiprocessing later 
# =============================================================================
    if (time.time()-frametime) >= (1/60):
        frame_counter += 1
        frametime = time.time()
    
    if frame_counter == frames_per_gridcell:
        try: 
            frame_counter = 0
            dummy_board = board.copy()
            dummy_board[height:30+height, 0:30] = t_piece
            height += atom_size
            
        except:
            height = 0
        
    
# =============================================================================
#   event handler
# =============================================================================
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                print('keydown')
                displ_bool = not displ_bool
                
# =============================================================================
#   only draw to screen when specified
# =============================================================================
    if displ_bool:    
        board_game = pygame.pixelcopy.make_surface(dummy_board)
        flipped = pygame.transform.flip(board_game, True, False)
        rotated = pygame.transform.rotate(flipped, 90)
        scaled_win = pygame.transform.scale(rotated, screen.get_size())
        screen.blit(scaled_win, (0,0))
        pygame.display.update()
        
