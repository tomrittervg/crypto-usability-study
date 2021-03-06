#!/usr/bin/env python

import os

def fourSplit(s):
    return s[0:4] + " " + s[4:8] + " " + s[8:12] + " " + s[12:16] + "  " + \
        s[16:20] + " " + s[20:24] + " " + s[24:28] + " " + s[28:32]

def genData():
    r = []
    
    #Use secure random, cause why not
    base = os.urandom(16)
    hexbytes = [hex(ord(b))[2:] for b in base]
    hexbytes = ['0' + c if len(c) == 1 else c for c in hexbytes]
    base = "".join(hexbytes).upper()
    r.append(fourSplit(base))
    
    #A 2^80 match will have 20 characters in common. 
    #  Flip exactly 12 spaces to a random value...
    #  Which might be the current value it is
    places_to_flip = []
    while len(places_to_flip) < 12:
        place = ord(os.urandom(1)) % 32
        if place not in places_to_flip:
            places_to_flip.append(place)
    rand_difference = list(base)
    for i in places_to_flip:
        rand_difference[i] = hex(ord(os.urandom(1)) % 16)[2:].upper()
    r.append(fourSplit("".join(rand_difference)))
    
    return r

if __name__ == "__main__":
    for i in genData():
        print i
    
