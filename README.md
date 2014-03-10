== About ==

If we can, some mailing list junkies including Tom Ritter, Trevor Perrin, and other folks at [messaging]() are going to try and run a usability study of different authentication mechanisms.

== Overall Goal ==

We have a bajillion things we'd like to run a usability study on, but to start somewhere and not overextend ourselves, let's focus on a single scenario: comparing 'fingerprints' of public keys, with three variables:
 - fingerprint type (hexadecimal digits, base64, etc)
 - comparison mechanism (business card, read aloud, another screen) 
 - error rates of the fingerprints (perfect match, one subtle flaw, one computationally determined flaw)

== Fingerprint Types ==

We suggest the following types of fingerprint types.  There are certainly more, but the more we try to test the bigger we're making it.

1) Hexadecimal digits ala PGP fingerprints: 8ACD 146E A94C EB12 E4EA  6915 66A1 0918 9B79 658F
2) Pseudowords
3) English Words

== Comparison Mechanisms ==

We suggest the following types of comparison mechanisms:

1) Business Cards
2) Spoken Aloud Over a Cell Phone

We believe the error rate of speaking aloud over a cell phone will be at least as great, if not greater, than spoken aloud in the same room.  Accordingly, we think we can cut that out.  

Similarly, comparing two fingerprints on two screens is either done with two people or not. If it's done with two people, it can be reduced to spoken aloud.  If it's between two of your own devices, we propose that most of this time it's _not_ between two laptops or full-screen monitors, but rather between a phone and a screen.  This is very similar to the business card scenario.  

In the future, other comparison mechanisms can be added. For now, let's try to avoid adding too many dimensions to the matrix.

== Approaches ==

Not knowing much about usability studies, I can see two approaches we could take.  

'Head Fake' approach.  In this approach, the subject does _not_ know we are testing how well they can compare the fingerprint. They have as much time for the task as they wish, but they are somehow led to believe that the comparison is not the primary goal. 

Time-Gated or Repeat-Gated approach. In this approach, the subject knows (or it is otherwise obvious to them) that we are testing how well they can compare the fingerprint. 
For the Business Card scenario, we give them a variable amount of time to do so, and measure if it was a successful determination or not after that time is elapsed.
For the Spoke Aloud scenario, we read it aloud to them once at a constant speed.

It seems that the Head Fake approach is more likely to produce real world results. In the real world, people will have as much time for the task as they want to have, but will have no exterior pressure to get a 'right' answer.  But, the Head Fake approach is much more difficult to engineer, as it relies on the subjects not detecting the head fake.  The Time-Gated approach tries to trade off for the knowledge of the test by the time limit.  

I have no idea if such a trade off is an accurate representation of the real world.

== Modulating Speed ==

To ensure that the fingerprint is spoken aloud at the same speed, every time, we will show the fingerprint, one token at a time (one hex digit or one word), in a video. The speaker cannot move faster than the length of the frame as they won't know the next token.  (They may memorize it, but regardless the frame will keep them to the same time.) 

== Error Rates ==

We suggest the following error rates:

 - Perfect Match (the fingerprints are perfect match)
 - One Subtle Flaw (the fingerprints differ by a single token chosen specifically to be confused. For example when speaking aloud B and C,D,E,3 or 8 and A)
 - One computationally chosen flaw:

To create the computationally chosen flaw, we will take a target fingerprint and generate as many random fingerprints as possible trying to match it by a chosen algorithm.  This will need a bit of fleshing out, but basically we run the SSH fingerprint look-alike tool.

I suspect that the computationally chosen flaw would have vastly different success rates in the 'Head Fake' approach than the Time-Gated approach.

== Test Matrix ==

  3 Fingerprint Types
  2 Comparison Mechanisms
x 3 Error Rates
---
 18 Test Cases / Subject