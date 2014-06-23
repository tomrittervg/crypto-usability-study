
"""
s = open("diceware.words").read()
s2 = s.split("\n")
s3 = [s[6:] for s in s2]
print '",\n"'.join(s3)
"""


from basic_english_words import words
try:
    from bitstring import BitArray
except:
    raise Exception("Please 'easy_install bitstring' - I trust its code more than my own")
import random, os

def getFpr():
    r = random.Random()
    chosen_words = []
    for x in range(13):
        chosen_words.append(r.choice(words))
    return chosen_words

def make_int(start_byte, start_bit, bytearray):
    b = BitArray(bytes="".join(bytearray), length=9, offset=(8*start_byte)+start_bit)
    start_bit += 9
    if start_bit >= 16:
        start_byte += 2
    elif start_bit >= 8:
        start_byte += 1
    else:
        raise Exception("Should not happen")
    start_bit %= 8
    return start_byte, start_bit, b.uint

def encode_fingerprint(rand_bytearray):
    start_byte = 0
    start_bit = 0
    fpr = []
    for x in range(14):
        start_byte, start_bit, indx = make_int(start_byte, start_bit, rand_bytearray)
        fpr.append(words[indx])
    return fpr
    
def genData():
    #There are 512 words, 14 makes a 126 bit fingerprint
    # 512^13 ~= 1.6615349947311448411297588253504e+35
    # 2 ^126 ~= 8.5070591730234615865843651857942e+37
    # 512^14 ~= 8.5070591730234615865843651857942e+37
    # 2 ^127 ~= 1.7014118346046923173168730371588e+38
    # 2 ^128 ~= 3.4028236692093846346337460743177e+38
    # 850^14 ~= 1.027696695308843560791015625e+41

    fingerprints = []

    #Get the base fingerprint
    base_fingerprint = os.urandom(17)# First generate (at least) 126 bits for the fingerprint
    base = encode_fingerprint(base_fingerprint)
    fingerprints.append(" - ".join(base))

    #Now we want to simulate an adversary that can perform a 2^80 attack.  
    # Flip 126-80 = 46 of the bits
    # Question: should they be negated (that is, they don't match) or chosen randomly?
    #           not sure...
    method = "negated" #"random"

    r = random.Random()
    places_to_flip = []
    while len(places_to_flip) < 46:
        place = r.randrange(126)
        if place not in places_to_flip:
            places_to_flip.append(place)

    rand_difference = BitArray(bytes=base_fingerprint)
    for i in places_to_flip:
        if method == "negated":
            rand_difference[i] = not rand_difference[i]
        else:
            rand_difference[i] = ord(os.urandom(1)) & 0x01

    rand_difference = rand_difference.bytes
    rand_fpr = encode_fingerprint(rand_difference)
    fingerprints.append(" - ".join(rand_fpr))

    return fingerprints

def testVectors():
    assert( len(words) > 0b0111111111)
    
    b = BitArray(bytes=chr(0b10101010))
    assert(b[len(b)-1] == False)
    assert(b[len(b)-2] == True)
    b[len(b)-1] = not b[len(b)-1]
    b[len(b)-2] = not b[len(b)-2]
    assert(b[len(b)-1] == True)
    assert(b[len(b)-2] == False)
    
    
    assert((1, 1, 0b111111111) == make_int(0, 0, [chr(0b11111111), chr(0b11111111)]))
    assert((1, 1, 0b111111110) == make_int(0, 0, [chr(0b11111111), chr(0b01111111)]))
    assert((1, 1, 0b111111101) == make_int(0, 0, [chr(0b11111110), chr(0b11111111)]))
    assert((1, 1, 0b111111011) == make_int(0, 0, [chr(0b11111101), chr(0b11111111)]))
    
    assert((1, 5, 0b111111111) == make_int(0, 4, [chr(0b11111111), chr(0b11111111), chr(0b11111111), chr(0b11111111)]))
    
    assert((1, 6, 0b111111111) == make_int(0, 5, [chr(0b11111111), chr(0b11111111), chr(0b11111111), chr(0b11111111)]))
    assert((1, 7, 0b111111111) == make_int(0, 6, [chr(0b11111111), chr(0b11111111), chr(0b11111111), chr(0b11111111)]))
    assert((2, 0, 0b111111111) == make_int(0, 7, [chr(0b11111111), chr(0b11111111), chr(0b11111111), chr(0b11111111)]))
    assert((2, 1, 0b111111111) == make_int(1, 0, [chr(0b11111111), chr(0b11111111), chr(0b11111111), chr(0b11111111)]))
    assert((2, 2, 0b111111111) == make_int(1, 1, [chr(0b11111111), chr(0b11111111), chr(0b11111111), chr(0b11111111)]))

    assert((1, 6, 0b111111110) == make_int(0, 5, [chr(0b11111111), chr(0b11111011), chr(0b11111111), chr(0b11111111)]))
    assert((1, 7, 0b111111110) == make_int(0, 6, [chr(0b11111111), chr(0b11111101), chr(0b11111111), chr(0b11111111)]))
    assert((2, 0, 0b111111110) == make_int(0, 7, [chr(0b11111111), chr(0b11111110), chr(0b11111111), chr(0b11111111)]))
    assert((2, 1, 0b111111110) == make_int(1, 0, [chr(0b11111111), chr(0b11111111), chr(0b01111111), chr(0b11111111)]))
    assert((2, 2, 0b111111110) == make_int(1, 1, [chr(0b11111111), chr(0b11111111), chr(0b10111111), chr(0b11111111)]))

    assert((1, 6, 0b011111111) == make_int(0, 5, [chr(0b11111011), chr(0b11111111), chr(0b11111111), chr(0b11111111)]))
    assert((1, 7, 0b011111111) == make_int(0, 6, [chr(0b11111101), chr(0b11111111), chr(0b11111111), chr(0b11111111)]))
    assert((2, 0, 0b011111111) == make_int(0, 7, [chr(0b11111110), chr(0b11111111), chr(0b11111111), chr(0b11111111)]))
    assert((2, 1, 0b011111111) == make_int(1, 0, [chr(0b11111111), chr(0b01111111), chr(0b11111111), chr(0b11111111)]))
    assert((2, 2, 0b011111111) == make_int(1, 1, [chr(0b11111111), chr(0b10111111), chr(0b11111111), chr(0b11111111)]))
    
if __name__ == "__main__":
    testVectors()
    for i in genData():
        print '-------------------------------------'
        print i