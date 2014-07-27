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
 32 Test Cases
 
 Run: ./genTestData.py > testdata.csv"""




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
    print '#pair\tfingerprint\tcomparison\terror\tAlice\tBob\tjudgement'
    for tid in  range(testerpairs):
        for mech in comparisons:
            for errorDesc,errorFunc in errors.items():
                for fingerprintDesc,fingerprintFunc  in fingerprints.items():
                    for possibleOutcome in outcomes:
                        alicePrint,bobPrint=errorFunc(fingerprintFunc)
                        print '\t'.join([str(tid),fingerprintDesc,mech,errorDesc,alicePrint,bobPrint])


if __name__ == '__main__':
    genTestData()
    
    