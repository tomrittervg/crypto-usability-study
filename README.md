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
 2. Pseudowords (For example: djijeh - isoy - dacif - qipc - buyowa)
 3. English Words (For example: bridge - late - sister - plane - brush - error - cup - soup - organization - great - quality - offer - dead)
 4. English poems (See [example implementation](https://github.com/akwizgran/basic-english) and [example comparison](https://moderncrypto.org/mail-archive/messaging/2014/000125.html)
 5. Visual Fingerprints (Probably [unicorns](http://unicornify.appspot.com/making-of), but [other](https://sparrow.ece.cmu.edu/group/pub/old-pubs/validation.pdf) [possibilities exist](https://moderncrypto.org/mail-archive/messaging/2014/000089.html))

## Comparison Mechanisms

We suggest the following types of comparison mechanisms:

 1. Business Cards
 2. Spoken Aloud, between two participants, over a Cell Phone

While it's more common to have the two people in the same room, we believe the error rate of speaking aloud over a cell phone will be at least as great, if not greater, than spoken aloud in the same room, so we can just do it over the cell phone and not have them in the same room.

Similarly, comparing two fingerprints on two screens is either done with two people or not. If it's done with two people, it can be reduced to spoken aloud.  If it's between two of your own devices, we propose that most of this time it's _not_ between two laptops or full-screen monitors, but rather between a phone and a screen.  This is very similar to the business card scenario.  

In the future, other comparison mechanisms can be added. For now, let's try to avoid adding too many dimensions to the matrix.

## Approaches

When comparing between a business card and a screen, the subject will have a specified number of seconds to complete the comparison and give an answer. In this approach, the subject knows (or it is otherwise obvious to them) that we are testing how well they can compare the fingerprint. We will try to figure out an appropriate amount of time to give them by performing some preliminary testing.

When comparing aloud between two participants, we will give them as much time as they wish, but it will be between two participants and we will otherwise not interfere.  One will have a fingerprint on a business card, the other will have a fingerprint on a screen. They will talk to each other over cell phones, and the one with a screen will give us an answer when they are satisfied they have made a dtermination.

When comparing between two participants on the phone the tester will measure, in addition to a correct or incorrect determination, how many times the participants asks the other to repeat the last token, slow down, or otherwise change how they're reciting it.

## Error Rates

We suggest the following error rates:

 - Perfect Match (the fingerprints are perfect match)
 - One computationally chosen flaw of 2^80 complexity

To create the computationally chosen flaw, we will take a target fingerprint and 'cheat' to form a fingerprint that has approximately 2^80 computational match.  For each type this will be done slightly differently.

 - Hexadecimal Digits - have the middle N characters different
 - Pseudowords, English Words, Poems - Match the outer words, but have the inner words have a low but non-zero hamming distance (ideally taking into account pronunciation)
 - Unicorns - Match the color, position, and size of the unicorn within an epsilon estimated to be 2^80

## Test Matrix

      5 Fingerprint Types
      2 Comparison Mechanisms
      2 Error Rates
    x 2 Outcomes (Match or Not-Match)
    ---
     40 Test Cases

To avoid having every subject see an exact distribution of match and non-match for each type, each subject will get a randomly selected set of tests. The goal is that over N subjects, we will get a statistically valid and even distribution of trials for each category.
     
## Rejected Ideas

### The 'Head Fake Approach

In this approach, the subject does _not_ know we are testing how well they can compare the fingerprint. They have as much time for the task as they wish, but they are somehow led to believe that the comparison is not the primary goal. An experiment may have them do Task A, Task B, compare fingerprints so they can complete Task C, and then do Task D. The subject thinks we are measuring a different task, or all of the tasks, and is unaware we only care about the fingerprint comparison.

It seems that the Head Fake approach is more likely to produce real world results. In the real world, people will have as much time for the task as they want to have, but will have no exterior pressure to get a 'right' answer.  But, the Head Fake approach is much more difficult to engineer, as it relies on the subjects not detecting the head fake.  The Time-Gated approach tries to trade off for the knowledge of the test by the time limit.  
