#!/usr/bin/env python

from hexadecimal_testdata.hexdata import genData as hexData
from englishword_testdata.gen_basic import genData as englishWordData
from englishpoems_testdata.gendata import genData as englishPoemData
from pseudoword_testdata.keyname_script import genData as pseudoWordData

for f in hexData():
    print f
for f in englishWordData():
    print f
for f in englishPoemData():
    print f
for f in pseudoWordData():
    print f
