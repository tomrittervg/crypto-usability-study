#!/usr/bin/env python

from random import choice
import sys

from hexadecimal_testdata.hexdata import genData as hexData
from englishword_testdata.gen_basic import genData as englishWordData
from englishpoems_testdata.gendata import genData as englishPoemData
from pseudoword_testdata.keyname_script import genData as pseudoWordData

"""
4 Fingerprint Types (TODO: what happened to 5th?)
2 Comparison Mechanisms
2 Error Rates
x 2 Outcomes (Match or Not-Match)
---
32 Test Cases
 
Run: ./genTestData.py <testerpairs> > testData.csv
"""


def farFingerprintsToCompare(genData) :
    perfectMatch,almostMatch = genData()
    noMatch,noMatch =  genData()
    return perfectMatch,choice([perfectMatch,noMatch])
    
def closeFingerprintsToCompare(genData):
    perfectMatch,almostMatch = genData()
    noMatch,noMatch =  genData()
    return perfectMatch,choice([perfectMatch,almostMatch])

def normalize(s):
    return s.replace('\n','<br>').strip()
    

fingerprints = {'hex':hexData,'english word':englishWordData,'english poem':englishPoemData,'pseudo word':pseudoWordData}
comparisons = ['Business card','Phone']
errors = {'large mismatch':farFingerprintsToCompare,'small mismatch':closeFingerprintsToCompare}
outcomes = ['match','not match']

def genTestData(testerpairs):
    print '#pair\tfingerprint\tcomparison\terror\tAlice\tBob\tjudgement'
    for tid in  range(testerpairs):
        for mech in comparisons:
            for errorDesc,errorFunc in errors.items():
                for fingerprintDesc,fingerprintFunc  in fingerprints.items():
                    for possibleOutcome in outcomes:
                        alicePrint,bobPrint = errorFunc(fingerprintFunc)
                        print '\t'.join([str(tid),fingerprintDesc,mech,errorDesc,normalize(alicePrint),normalize(bobPrint)])


if __name__ == '__main__':
    genTestData(sys.argv[1])
    
    