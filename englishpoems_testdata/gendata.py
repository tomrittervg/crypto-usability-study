#!/usr/bin/env python

from time import time
import re, os
import random
import subprocess
from math import log

def getPoem():
    cmd = subprocess.Popen([os.path.join(os.path.dirname(os.path.realpath(__file__)), "basic-english.pl"), '128'], stdout=subprocess.PIPE)
    cmd_out, cmd_err = cmd.communicate()
    return cmd_out

f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "word-lists/basic-adjectives"), 'r')
adjectives = [ l.strip() for l in f.readlines()]
f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"word-lists/basic-adverbs"), 'r')
adverbs = [ l.strip() for l in f.readlines()]
f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"word-lists/basic-articles"), 'r')
articles = [ l.strip() for l in f.readlines()]
f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"word-lists/basic-nouns"), 'r')
nouns = [ l.strip() for l in f.readlines()]
f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"word-lists/basic-prepositions"), 'r')
prepositions = [ l.strip() for l in f.readlines()]
f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"word-lists/basic-verbs-i"), 'r')
verbsi = [ l.strip() for l in f.readlines()]
f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"word-lists/basic-verbs-t"), 'r')
verbst = [ l.strip() for l in f.readlines()]
    
def disassemble_type(words):
    selection = []
    for w in words:
        if w == '': 
            selection.append('PLACEHOLDER-FOR-NEWLINE')
        elif w in adjectives:
            selection.append(adjectives)
        elif w in adverbs:
            selection.append(adverbs)
        elif w in articles:
            selection.append(articles)
        elif w in nouns:
            selection.append(nouns)
        elif w in prepositions:
            selection.append(prepositions)
        elif w in verbsi:
            selection.append(verbsi)
        elif w in verbst:
            selection.append(verbst)
    return selection
def reconstruct_to_poem(words):
    s = ""
    for w in words:
        if w == '': s += "\n"
        else: s += w + " "
    return s
    
def genData():
    fingerprints = []

    #Get the base fingerprint
    base = re.split(' |\n', getPoem())
    fingerprints.append(reconstruct_to_poem(base))

    #Now we want to simulate an adversary that can perform a 2^80 attack. 
    #   This is not perfectly accurate, as the structure of the poem in fact 
    #   encodes some bits (Between 17 and 23 usually).
    #   So we're going to round that to 20, and assume the attacker 'spends' 20 
    #   of his bits achieving the same grammatical structure.  Again, not perfectly 
    #   accurate, but hpefully it won't be too far off.
    randomly_changed = base
    types = disassemble_type(base)
    bits = 0 #Start at 0 bits
    places_we_flipped = []

    while bits < (128-80): #Keep muttating until we've mutated at least 48 bits
                           #  This will keep the structure in tact, but change 48 bits of words
                           #  This is kind of confusing, but it's discussed at
                           #  https://github.com/tomrittervg/crypto-usability-study/issues/3#issuecomment-50423948
        #find a random position to replace
        place = random.randrange(len(randomly_changed))
        while place in places_we_flipped or randomly_changed[place].strip() == '':
            place = random.randrange(len(randomly_changed))
        places_we_flipped.append(place)
        #print place, randomly_changed[place], len(types[place])
        
        randomly_changed[place] = types[place][random.randrange(len(types[place]))]
        #subtract however many bits we estimate this selection point to be
        bits += log(len(types[place])) / log(2) 
        #print bits

    fingerprints.append(reconstruct_to_poem(randomly_changed))
    
    return fingerprints

if __name__ == "__main__":
    for i in genData():
        print '-------------------------------------'
        print i
