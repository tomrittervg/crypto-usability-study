#!/usr/bin/env python

from hexadecimal_testdata.hexdata import genData as hexData
from englishword_testdata.gen_basic import genData as englishWordData
from englishpoems_testdata.gendata import genData as englishPoemData
from pseudoword_testdata.keyname_script import genData as pseudoWordData
from random import choice

"""4 Fingerprint Types (TODO: what happened to 5th?)
2 Comparison Mechanisms
2 Error Rates
x 2 Outcomes (Match or Not-Match)
 ---
 32 Test Cases"""




def demo():
    for f in hexData():
        print f
    for f in englishWordData():
        print f
    for f in englishPoemData():
        print f
    for f in pseudoWordData():
        print f

def farFingerprintsToCompare(genData) :
    perfectMatch,almostMatch = genData()
    noMatch,noMatch =  genData()
    return perfectMatch,choice([perfectMatch,noMatch])
    
def closeFingerprintsToCompare(genData):
    perfectMatch,almostMatch = genData()
    noMatch,noMatch =  genData()
    return perfectMatch,choice([perfectMatch,almostMatch])
    


testerpairs=1
fingerprints = {'hex':hexData,'english word':englishWordData,'english poem':englishPoemData,'pseudo word':pseudoWordData}
comparisons = ['Business card','Phone']
errors = {'large mismatch':farFingerprintsToCompare,'small mismatch':closeFingerprintsToCompare }
outcomes = ['match','not match']

def genTestData():
    for tid in  range(testerpairs):
        print 'Tester pair %d tests' % tid
        for mech in comparisons:
            print mech
            for errorDesc,errorFunc in errors.items():
                print errorDesc
                for fingerprintDesc,fingerprintFunc  in fingerprints.items():
                    print fingerprintDesc
                    for possibleOutcome in outcomes:
                        alicePrint,bobPrint=errorFunc(fingerprintFunc)
                        print 'Alice:',alicePrint,' Bob:',bobPrint


if __name__ == '__main__':
    genTestData()
    
    