# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 15:17:43 2022

@author: Mathieu
"""

import itertools as ite

liste = [0,1,2,3,4]

permut = list(ite.permutations(liste))
print(permut)
print(len(permut))
print(permut[119])