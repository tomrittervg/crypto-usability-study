#!/usr/bin/env python

import os

def soundsLike(c):
    #TODO
    # Use http://stevehanov.ca/blog/index.php?id=8 or double metaphone 
    # to find rhyming words 
    if c == '1':
        return ['0']
    elif c == '2':
        return []
    elif c == '3':
        return ['B', 'C', 'D', 'E']
    elif c == '4':
        return ['5', 'F']
    elif c == '5':
        return ['4', 'F']
    elif c == '6':
        return ['7']
    elif c == '7':
        return ['6']
    elif c == '8':
        return ['A']
    elif c == '9':
        return []
    elif c == '0':
        return ['1']
    elif c == 'A':
        return ['8']
    elif c == 'B':
        return ['3', 'C', 'D', 'E']
    elif c == 'C':
        return ['3', 'B', 'D', 'E']
    elif c == 'D':
        return ['3', 'B', 'C', 'E']
    elif c == 'E':
        return ['3', 'B', 'C', 'D']
    elif c == 'F':
        return ['F']
    else:
        raise Exception("Unexpected character send to soundsLike")

def genData():
    r = []
    
    #Use secure random, cause why not
    base = os.urandom(16)
    hexbytes = [hex(ord(b))[2:] for b in base]
    hexbytes = ['0' + c if len(c) == 1 else c for c in hexbytes]
    base = "".join(hexbytes).upper()
    r.append(base)
    
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
    r.append("".join(rand_difference))
    
    #Now flip the N spaces in the middle.
    # TODO!!
    # We assume an adversary who can do 2^80. But matching 
    # exactly the outer 10 costs more than 2^80. So how unmatched 
    # numbers in the middle and matches on the outside calculate 
    # to a 2^80 attacker?  I don't know yet.
    middle_difference = list(base    )
    for i in range(10,22):
        middle_difference[i] = hex(ord(os.urandom(1)) % 16)[2:].upper()
    r.append("".join(middle_difference))
    
    #Now the tricky part. We assume an attacker who can do 2^80
    # Have N unmatched-but-phonetically-similar letters, where N
    # will be greater than 12, but how _many_ more than twelve.
    # I also don't know that yet!
    # TODO
    places_to_flip = []
    while len(places_to_flip) < 12:
        place = ord(os.urandom(1)) % 32
        if place not in places_to_flip:
            places_to_flip.append(place)
    phonetic_difference = list(base)
    for i in places_to_flip:
        char = soundsLike(phonetic_difference[i])
        if len(char) > 0:
            char = char[ord(os.urandom(1)) % len(char)]
        else:
            char = hex(ord(os.urandom(1)) % 16)[2:].upper()
        phonetic_difference[i] = char
    r.append("".join(phonetic_difference))
    
    return r

if __name__ == "__main__":
    for i in genData():
        print i
    