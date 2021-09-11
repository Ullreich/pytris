#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 13:59:18 2021

@author: ferdinand
"""
import numpy as np
import matplotlib.pyplot as plt

# original nes: 256x240

# set color and dim
color1 = [103, 144, 255]
color2 = [72,61,139]
color3 = [218,152,235]
color4 = [64,214,208]
color5 = [34,139,34]
color6 = [255,79,51]
color7 = [194,124,11]


dims = 10

#-----------------------------------------------------------------------------
# two different types of atoms for the tetrominos
#-----------------------------------------------------------------------------
atom1_bool = np.ones(shape=(dims,dims), dtype='bool')
# fancy whites
atom1_bool[1,1:4] = False
atom1_bool[2,1:3] = False
atom1_bool[3,1] = False
atom1_bool[0,0] = False

atom2_bool = np.ones(shape=(dims,dims), dtype='bool')
# fancy whites
atom2_bool[1:-1, 1:-1] = False
atom2_bool[0,0] = False


def build_atom(atom1_bool, colors):
    test = np.ones(shape=(dims,dims,3), dtype='int64')*255
    test[atom1_bool] = colors
    return test

def build_block(black, piece):
    block = np.r_[np.concatenate([piece, piece, piece], 1),
                  np.concatenate([black, piece, black], 1),
                  np.concatenate([black, black, black], 1)]
    return block

#-----------------------------------------------------------------------------
# make filler and atoms
#-----------------------------------------------------------------------------
black = np.zeros((dims,dims,3), dtype="int64")
piece = build_atom(atom2_bool, color6)


block = build_block(black, piece)
plt.imshow(block)

