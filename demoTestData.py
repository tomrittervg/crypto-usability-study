#!/usr/bin/env python

from hexadecimal_testdata.hexdata import genData as hexData
from englishword_testdata.gen_basic import genData as englishWordData
from englishpoems_testdata.gendata import genData as englishPoemData
from pseudoword_testdata.keyname_script import genData as pseudoWordData

print "#1. Hexadecimal digits ala PGP fingerprints"
for f in hexData():
    print f
print "#2. English Words"
for f in englishWordData():
    print f
print "#3. English poems"
for f in englishPoemData():
    print f
print "#4. Pseudowords"
for f in pseudoWordData():
    print f
