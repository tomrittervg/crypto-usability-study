

from time import time
import os
import binascii
import subprocess
import math

def run_test(num_trials, max_iters, target_score, print_all=False):
	itersList = []
	#print("num_trials = %d max_iters=%d target_score=%d" % (num_trials, max_iters, target_score))
	for x in range(num_trials):
		pseudokey = binascii.b2a_hex(os.urandom(16))
		cmd = subprocess.Popen(["./keyname", pseudokey, str(max_iters), str(target_score)], stdout=subprocess.PIPE)
		cmd_out, cmd_err = cmd.communicate()
		idx = cmd_out[:-1].rfind("\n")
		iters = int(cmd_out[idx+1:])
		itersList.append(iters)
        
        fingerprint = cmd_out.split('\n')[-4]
        return fingerprint


def format_pseudoword(str):
    return str[0:6] + " - " + str[6:10] + " - " + str[10:15] + " - " + str[15:19] + " - " + str[20:]
    
alphabet = "abcdefghijklmnopqrstuvwxyz234567"
      
fingerprints = []
      
#First get the base pseudoword fingerprint.
base = run_test(1, 1100000000, 17, True).replace(" - ", "")
fingerprints.append(format_pseudoword(base))

#Now we want to simulate an adversary that can perform a 2^80 attack.  This means
# the attacker cannot match 9 or 10 of the 25 characters.  Flip those 10
places_to_flip = []
while len(places_to_flip) < 12:
    place = ord(os.urandom(1)) % 25
    if place not in places_to_flip:
        places_to_flip.append(place)
rand_difference = list(base)
for i in places_to_flip:
    rand_difference[i] = alphabet[ord(os.urandom(1)) % len(alphabet)]
fingerprints.append(format_pseudoword("".join(rand_difference)))

#Now we want to simulate an attacker flipping the innermost N spaces
#TODO

#And flipping characters such that they sound phonetically similar
#TODO

for f in fingerprints:
    print f