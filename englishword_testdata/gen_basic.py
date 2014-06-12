
"""
s = open("diceware.words").read()
s2 = s.split("\n")
s3 = [s[6:] for s in s2]
print '",\n"'.join(s3)
"""


from basic_english_words import words
import random

def getFpr():
    r = random.Random()
    chosen_words = []
    for x in range(13):
        chosen_words.append(r.choice(words))
    return chosen_words

def genData():
    #There are 850 words, 13 makes an approximately 127 bit fingerprint
    # 850^12 ~= 1.42241757136172119140625e+35
    # 2 ^126 ~= 8.5070591730234615865843651857942e+37
    # 850^13 ~= 1.2090549356574630126953125e+38
    # 2 ^127 ~= 1.7014118346046923173168730371588e+38
    # 2 ^128 ~= 3.4028236692093846346337460743177e+38
    # 850^14 ~= 1.027696695308843560791015625e+41

    fingerprints = []

    #Get the base fingerprint
    base = getFpr()
    fingerprints.append(" - ".join(base))

    #Now we want to simulate an adversary that can perform a 2^80 attack.  
    # This equates to matching 8 or 9 of the words.  We'll say 8. Flip 5

    r = random.Random()
    places_to_flip = []
    while len(places_to_flip) < 5:
        place = r.randrange(13)
        if place not in places_to_flip:
            places_to_flip.append(place)

    rand_difference = base
    for i in places_to_flip:
        rand_difference[i] = r.choice(words)

    fingerprints.append(" - ".join(rand_difference))

    return fingerprints
    
if __name__ == "__main__":
    for i in genData():
        print '-------------------------------------'
        print i