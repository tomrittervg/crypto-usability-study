## About

If we can, some mailing list junkies including Tom Ritter, Trevor Perrin, Christine Corbett and other folks at [messaging](http://moderncrypto.org/) are going to try and run a usability study of different authentication mechanisms.

## Overall Goal

We have a bajillion things we'd like to run a usability study on, but to start somewhere and not overextend ourselves, let's focus on a single scenario: comparing 'fingerprints' of public keys, with three variables:
 - fingerprint type (hexadecimal digits, base64, etc)
 - comparison mechanism (business card, read aloud, another screen) 
 - error rates of the fingerprints (perfect match vs a 2^80-capable attacker)

## Fingerprint Types

We suggest the following types of fingerprint types.  There are certainly more, but the more we try to test the bigger we're making it.

 1. Hexadecimal digits ala PGP fingerprints: 8ACD 146E A94C EB12 E4EA  6915 66A1 0918 9B79 658F
 2. English Words (For example: bridge - late - sister - plane - brush - error - cup - soup - organization - great - quality - offer - dead)
 3. English poems (See [example implementation](https://github.com/akwizgran/basic-english) and [example comparison](https://moderncrypto.org/mail-archive/messaging/2014/000125.html) 
 4. Pseudowords (For example: djijeh - isoy - dacif - qipc - buyowa)
 5. Visual Fingerprints (Using OpenSSH's [visual host keys](http://www.kcbug.org/?p=18))

## Comparison Mechanisms

We suggest the following types of comparison mechanisms:

 1. Business Cards
 2. Spoken Aloud, between two participants, over a Cell Phone or Landline

While it's more common to have the two people in the same room, we believe the error rate of speaking aloud over a phone will be at least as great, if not greater, than spoken aloud in the same room, so we can just do it over the phone and not have them in the same room.  However, should it be a cell phone or a landline? If it's a cell phone, the error rate will be greater and potentially a harsher test (this being desirable) - but will the cell phone reception variability introduce unacceptable variables?

Similarly, comparing two fingerprints on two screens is either done with two people or not. If it's done with two people, it can be reduced to spoken aloud.  If it's between two of your own devices, we propose that most of this time it's _not_ between two laptops or full-screen monitors, but rather between a phone and a screen.  This is very similar to the business card scenario.  

In the future, other comparison mechanisms can be added, such as having participants write the fingerprint in their own handwriting. For now, let's try to avoid adding too many dimensions to the matrix.

## Approaches

When comparing between a business card and a screen, the subject will have a specified number of seconds to complete the comparison and give an answer. In this approach, the subject knows (or it is otherwise obvious to them) that we are testing how well they can compare the fingerprint. 

When comparing aloud between two participants it will be between two participants and we will otherwise not interfere except to impose a time limit. One will have a fingerprint on a business card, the other will have a fingerprint on a screen. They will talk to each other over cell phones, and the one with a screen will give us an answer when they are satisfied they have made a dtermination.  We will try to figure out an appropriate amount of time to give them by performing some preliminary testing.

When comparing between two participants on the phone the tester will measure, in addition to a correct or incorrect determination, how long the participants make a determination prior to the time limit expiring.

## Error Rates

We suggest the following error rates:

 - Perfect Match (the fingerprints are perfect match)
 - One computationally chosen flaw of 2^80 complexity

To create the computationally chosen flaw, we will take a target fingerprint and 'cheat' to form a fingerprint that has approximately 2^80 computational match.  For each type this will be done slightly differently, but in the general case, I'm proposing 25% chance the imposter matches to a @^80 factor by an attribute deemed subjectively 'most likely to be noticed quickly by skimming', and a 75% chance it's entirely random.

 - Hexadecimal Digits - have N characters different, with the most skimmable attribute being the outer characters.
 - Pseudowords, English Words, Poems - The most skimmable attribute is matching the outer words, but having the inner words have a low but non-zero hamming distance (ideally taking into account pronunciation)
 - Visual Fingerprint - The most skimmable attribute is matching the position of characters, but ignoring the type

## Test Matrix

      5 Fingerprint Types
      2 Comparison Mechanisms
      2 Error Rates
    x 2 Outcomes (Match or Not-Match)
    ---
     40 Test Cases

To avoid having every subject see an exact distribution of match and non-match for each type, each subject will get a randomly selected set of tests. The goal is that over N subjects, we will get a statistically valid and even distribution of trials for each category.
     
## Test generation

 1. `cd pseudoword_testdata; make; cd ..`
 2. `python genTestData.python`
 Generates
 ```
 #1. Hexadecimal digits ala PGP fingerprints
 9F7B726D789BEB58D3E2FD79131C92AC
 397B02CD789BE55033E2BD7B121F52AC
 #2. English Words
 living - plate - receipt - limit - rat - organization - toe - rub - road - before - attraction - light - scissors
 living - discovery - receipt - limit - church - organization - cart - exchange - road - surprise - attraction - light - scissors

 #3. English poems
 his dead system rests widely from her true map
 this flat power decides on the tight walk with his shelf


 her rough system sits widely from her round map
 this clear pull wins across your smooth walk to our shelf

 #4. Pseudowords (For example: djijeh - isoy - dacif - qipc - buyowa)
 toswoc - ivuf - nayan - pem2 - atakg
 5esiku - ivug - aa5an - pewh - ataog
 ```
 

## Rejected Ideas

### The 'Head Fake Approach

In this approach, the subject does _not_ know we are testing how well they can compare the fingerprint. They have as much time for the task as they wish, but they are somehow led to believe that the comparison is not the primary goal. An experiment may have them do Task A, Task B, compare fingerprints so they can complete Task C, and then do Task D. The subject thinks we are measuring a different task, or all of the tasks, and is unaware we only care about the fingerprint comparison.

It seems that the Head Fake approach is more likely to produce real world results. In the real world, people will have as much time for the task as they want to have, but will have no exterior pressure to get a 'right' answer.  But, the Head Fake approach is much more difficult to engineer, as it relies on the subjects not detecting the head fake.  The Time-Gated approach tries to trade off for the knowledge of the test by the time limit.  
