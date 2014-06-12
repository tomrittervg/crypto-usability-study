

"Pseudoword" fingerprints
====

Users sometimes have to compare, transcribe, and read aloud public-key fingerprints.  Typical fingerprints are hard to use:

    SSH:  43:51:43:a1:b5:fc:8b:b7:0a:3a:a9:b1:0f:66:73:a8

    GPG:  7213 5CAA EA6B 0980 126A  0371 8373 DD15 4D42 48BD

    OTR:  C4E40F71 A92175F8 597A29A7 CB7E0943 B27014FF

We are hoping to improve useability with "pseudowords".  On generating a new keypair, the user's computer will spend several seconds searching for a fingerprint whose pseudowords have a high "score".  For example:

    Score=17:   wuvovr - tir3 - niruv - peng - hibita
    
    Score=17:   byadep - mayo - eqcni - idah - logutu

    Score=17:   hheute - ixej - urufe - unit - qefaiv

    Score=18:   duconi - huho - baj5w - yejo - epevig

    Score=18:   ezobiv - wxax - zugar - 2ube - adijuv

    Score=18:   7yilun - isub - ezinx - axaj - ifoyel   

In particular:
 * Base32 (RFC 4648) is chosen to encode the public key's hash.
     * This consists of 26 letters and 6 numbers.  The bias towards letters in RFC 4648 is helpful for forming pseudowords.
 * 25 characters are grouped into pseudowords of length 6-4-5-4-6.  
     * 25 base32 characters encodes a hash prefix of 125 bits, which gives adequate security.
     * The pseudowords have varying lengths to aid in detecting transcription errors.
     * The longest pseudowords are placed at the beginning and end, since those are most likely to be checked when users are performing visual comparison.
     * No pseudowords of the same length are adjacent.  

To create a new fingerprint, we append counters to the public key and SHA256 hash the result.   The resulting hash is encoded as base32, and assigned a "score" equal to the number of consonant/vowel and vowel/consonant transitions in each pseudoword.  This process is repeated until a fingerprint is discovered with an adequate score:

    best_score =  5, iters =          1   agh6ib - 57ut - 4jf2x - n4zm - xqsan5
    best_score =  6, iters =          8   agamqs - tufs - osgqv - kd42 - dsdt7y
    best_score =  7, iters =         15   h6euja - eh5b - uel4q - ssap - ajmqnd
    best_score =  8, iters =         17   fkalss - 6di7 - 55obb - zhit - yuvzgj
    best_score = 10, iters =        200   t2sahh - 5zwf - imuof - utoh - domsp3
    best_score = 11, iters =        455   maqofl - epyo - cqgnh - fpos - x6ufif
    best_score = 12, iters =       1545   mpowiw - tcop - yaleb - 26aj - 4ugqs2
    best_score = 13, iters =      11836   nafsbj - sicv - kepri - nekw - nepeuh
    best_score = 14, iters =      21574   yipazm - jvlx - adib7 - jifu - zekaxv
    best_score = 15, iters =      29872   5pifiy - gwil - ruqad - uiuv - ofoji5
    best_score = 16, iters =     452824   lavbis - viwp - ajweb - xoli - xmejis
    best_score = 17, iters =    4443784   umqahj - guli - lagub - upeh - wefjif
    best_score = 18, iters =   14352196   duconi - huho - baj5w - yejo - epevig

On my Macbook Air, this code can make close to 2 million trials per second per core.  With 10 million trials, it finds a score=17 ~80% of the time.  With 100 million trials, it finds a score=18 ~80% of the time.

Acknowledgements
===
Based on discussions on the messaging@moderncrypto.org mailing list.  In particular, Robert Ransom suggested using variable-sized chunks, and Nathan Wilcox suggested searching for fingerprints that users like more.
