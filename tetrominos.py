#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 21:47:46 2021

@author: ferdinand
"""
import numpy as np

# =============================================================================
# class for the board
# =============================================================================

class Board:
    def __init__(self, dims):
        self.dims = dims
        self.board = self.makeboard()
        self.background = np.load("background.npy")
        self.piece = self.select_piece()
        self.x = dims*6
        self.y = 0
        self.game_over = False
        self.score = 0
        self.score_list = [40, 100, 300, 1200]
        self.level = 0
        self.total_lines = 0
        self.fpg = 48 #frames per gridcell
        #speeds taken from https://harddrop.com/wiki/Tetris_(NES,_Nintendo)
        self.fpg_list = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5]
            
    # make the board with the boarders
    def makeboard(self):
        board = np.ones((self.dims*22, self.dims*14, 3), dtype="int64")*255
        board[:self.dims*20,self.dims*2:self.dims*12,:] = 0 
        
        return board
    
    def  select_piece(self):
        pieces = [T_Piece(self.dims).piece,
                  L_Piece(self.dims).piece,
                  J_Piece(self.dims).piece,
                  S_Piece(self.dims).piece,
                  Z_Piece(self.dims).piece,
                  I_Piece(self.dims).piece,
                  O_Piece(self.dims).piece]
        
        return np.random.choice(pieces)
    
    def spawn_new_piece(self):
        self.piece = self.select_piece()
        self.x = self.dims*6
        self.y = 0
        if self.collison():
            self.game_over = True
            
    
    def move_left(self):
        self.x -= self.dims
        if self.collison():
            self.x += self.dims
        
        
    def move_right(self):
        self.x += self.dims
        if self.collison():
            self.x -= self.dims
            
    def move_down(self):
        self.y += self.dims
        if self.collison():
            self.y -= self.dims
            # add piece to board
            self.board[self.y:self.y+self.piece.shape[0], self.x:self.x+self.piece.shape[1],:] += self.piece
            # look if there are full lines to delete
            self.delete_lines()
            # reset stuff
            self.spawn_new_piece()
    
    def rotate(self):
        if ((self.x + self.piece.shape[0]) <= self.dims*14) and ((self.y + self.piece.shape[1]) <= self.dims*22):
            try:
                self.piece = np.rot90(self.piece)
                if self.collison():
                    self.piece = np.rot90(self.piece, axes=(1,0))
            except:
                pass
            
    def delete_lines(self):
        # idea: iterate through lines and find full lines
        how_many = 0
        for i in range(0, self.dims*20, self.dims):
            # make a boolean array to check if there is an epty atom
            current_line = np.array(np.amax(self.board[i,:,:], 1), dtype="bool")
            if False not in current_line: # this indicates there is no empty atom in the line
                # increment how many filled lines
                how_many += 1
                #concatenate in between and add a white on top
                filler = np.zeros((self.dims,self.dims*14,3), dtype="int64")
                filler[:, :self.dims*2, :] = 255
                filler[:, self.dims*12:, :] = 255
                
                self.board = np.concatenate((filler, self.board[:i,:,:], self.board[i+self.dims:,:,:]))
        #score based on https://harddrop.com/wiki/Scoring
        #if lines are actually deleted
        if how_many > 0:
            self.score += self.score_list[how_many-1]*(self.level+1)
            #increment total deleted lines
            self.total_lines += how_many
            #increse level if we need to
            self.increase_level()
        
    def increase_level(self):
        #based on https://tetris.fandom.com/wiki/Tetris_(NES,_Nintendo)
        #check to see if level needs to be increased
        if self.total_lines >= ((self.level*10+10) or np.max([100, self.level*10-50])):
            #set back lines
            self.total_lines = self.total_lines%10
            #increase level
            self.level += 1
            #increase fpg
            if self.level <= 10:
                self.fpg = self.fpg_list[self.level]
            elif 10<self.level<=12:
                self.fpg = 5
            elif 13<=self.level<=15:
                self.fpg = 4
            elif 16<=self.level<=18:
                self.fpg = 3
            elif 19<=self.level<=28:
                self.fpg = 2
            else:
                self.fpg = 1
            print("speedup")
            print(self.fpg)
    
            
    def collison(self):
        # idea: get the first 3 colors of each atom
        # if one is not 0 make True
        # do the same with the board at those indexes.
        # if both are True at the same index we have a collison
        x_p = self.piece.shape[1]
        y_p = self.piece.shape[0]
        piece = self.piece[0:y_p:self.dims, 0:x_p:self.dims,:]
        piece = np.array(np.amax(piece, 2), dtype="bool")
        
        board_part = self.board[self.y:self.y+y_p:self.dims, self.x:self.x+x_p:self.dims,:]
        board_part = np.array(np.amax(board_part, 2), dtype="bool")
        
        if np.logical_and(piece, board_part).any():
            return True
        return False
    
    def final_array(self, dummy_board):
        arr = self.background
        #blit in board to background
        arr[:,100:200,:] = dummy_board
        
        return arr
        
    
# =============================================================================
# base class from which all others inherit 
# =============================================================================
class _Tetromino:
    def __init__(self, dims):
        self.dims = dims
        self.atom_filled = self._make_atom_filled()
        self.atom_empty = self._make_atom_empty()
        self.atom_black = np.zeros((dims,dims,3), dtype="int64")

    
    #needed to make a pretty atom block
    def _make_atom_filled(self):
        
        #old design
        atom1_bool = np.ones(shape=(self.dims, self.dims), dtype='bool')
        atom1_bool[1,1:4] = False
        atom1_bool[2,1:3] = False
        atom1_bool[3,1] = False
        atom1_bool[0,0] = False
        '''
        atom1_bool = np.ones(shape=(self.dims, self.dims), dtype='bool')
        
        #outside corners
        atom1_bool[1,1:3] = False
        atom1_bool[2,1] = False
        
        atom1_bool[self.dims-2,self.dims-3:self.dims-1] = False
        atom1_bool[self.dims-3,self.dims-2] = False
        
        #atom1_bool[1,self.dims-3:self.dims-1] = False
        #atom1_bool[2,self.dims-2] = False
        
        #atom1_bool[self.dims-2,1:3] = False
        #atom1_bool[self.dims-3,1] = False
        
        #if self.dims%2 == 0:
        #    atom1_bool[int(self.dims/2-1):int(self.dims/2+1),int(self.dims/2-1):int(self.dims/2+1)] = False
        '''
        return atom1_bool
    
    def _make_atom_empty(self):
        atom2_bool = np.ones(shape=(self.dims, self.dims), dtype='bool')
        atom2_bool[1:-1, 1:-1] = False
        atom2_bool[0,0] = False
        return atom2_bool
    
    # construct a 3d atom array
    def build_atom(self, atom, colors):
        atom_to_be = np.ones(shape=(self.dims,self.dims,3), dtype='int64')*255
        atom_to_be[atom] = colors
        return atom_to_be
    
    def build_block(self, p_a):
        '''
        Parameters
        ----------
        p_a : piece array; a np array of atoms in the shape of the tetromino

        Returns
        -------
        block : returns a colored tetromino np array

        '''
        # list comprehension: concat all rows
        row_list = [np.concatenate(row, 1) for row in p_a[:]]
        # concat columns
        block = np.concatenate(row_list[:])
        return block
    
# =============================================================================
# tetrominos
# rotations based on https://harddrop.com/wiki/Nintendo_Rotation_System
# rotation deviates from classic tetris
# =============================================================================

class T_Piece(_Tetromino):
    def __init__(self, dims):
        super().__init__(dims)
        self.color = [103, 144, 255]
        self.atom = self.build_atom(self.atom_empty, self.color)
        #make the tetromino
        a = self.atom           # asign a s that the piece array is less ugly
        b = self.atom_black
        piece_array = np.array([[b, a, b],
                                [a, a, a],
                                [b, b, b]])
        self.piece = self.build_block(piece_array)
        
class O_Piece(_Tetromino):
    def __init__(self, dims):
        super().__init__(dims)
        self.color = [72,61,139]
        self.atom = self.build_atom(self.atom_empty, self.color)
        #make the tetromino
        a = self.atom           # asign a s that the piece array is less ugly
        piece_array = np.array([[a, a],
                                [a, a]])
        self.piece = self.build_block(piece_array)
        
class I_Piece(_Tetromino):
    def __init__(self, dims):
        super().__init__(dims)
        self.color = [218,152,235]
        self.atom = self.build_atom(self.atom_empty, self.color)
        #make the tetromino
        a = self.atom           # asign a s that the piece array is less ugly
        b = self.atom_black
        piece_array = np.array([[b, a, b], 
                                [b, a, b],
                                [b, a, b],
                                [b, a, b]])
        self.piece = self.build_block(piece_array)
        
class L_Piece(_Tetromino):
    def __init__(self, dims):
        super().__init__(dims)
        self.color = [64,214,208]
        self.atom = self.build_atom(self.atom_filled, self.color)
        #make the tetromino
        a = self.atom           # asign a s that the piece array is less ugly
        b = self.atom_black
        piece_array = np.array([
                                [a, a, a], 
                                [a, b, b],
                                [b, b, b]])
        self.piece = self.build_block(piece_array)
        
class J_Piece(_Tetromino):
    def __init__(self, dims):
        super().__init__(dims)
        self.color = [34,139,34]
        self.atom = self.build_atom(self.atom_filled, self.color)
        #make the tetromino
        a = self.atom           # asign a s that the piece array is less ugly
        b = self.atom_black
        piece_array = np.array([[a, b, b], 
                                [a, a, a],
                                [b, b, b]])
        self.piece = self.build_block(piece_array)
        
class S_Piece(_Tetromino):
    def __init__(self, dims):
        super().__init__(dims)
        self.color = [255,79,51]
        self.atom = self.build_atom(self.atom_filled, self.color)
        #make the tetromino
        a = self.atom           # asign a s that the piece array is less ugly
        b = self.atom_black
        piece_array = np.array([[b, a, a],
                                [a, a, b], 
                                [b, b, b]])
        self.piece = self.build_block(piece_array)
        
class Z_Piece(_Tetromino):
    def __init__(self, dims):
        super().__init__(dims)
        self.color = [194,124,11]
        self.atom = self.build_atom(self.atom_filled, self.color)
        #make the tetromino
        a = self.atom           # asign a s that the piece array is less ugly
        b = self.atom_black
        piece_array = np.array([[a, a, b], 
                                [b, a, a],
                                [b, b, b]])
        self.piece = self.build_block(piece_array)
        
# =============================================================================
# test stuff
# =============================================================================
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import time
    
    dim = 10
    
    """
    T = T_Piece(10)
    L = L_Piece(10)
    J = J_Piece(10)
    S = S_Piece(10)
    Z = Z_Piece(10)
    I = I_Piece(10)
    O = O_Piece(10)
    
    pieces = [T, L, J, S, Z, I, O]
    
    for piece in pieces:
        print(piece)
        #plt.imshow(piece.block)
        time.sleep(1)
    """
    
    board = Board(10)
    dims=10
    plt.imshow(board.piece)
    
    dummy_board = board.board[:20*dims,2*dims:12*dims,:]
    #plt.imshow(dummy_board)
    with_background = board.final_array(dummy_board)
    plt.imshow(with_background)
    
    
    print(np.max(with_background))
    