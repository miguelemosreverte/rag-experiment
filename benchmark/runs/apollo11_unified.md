# Apollo 11 Unified Benchmark

**2026-04-02T09:38:00.568687** | **gemma-3-4b-it** | 370,778 tokens | 725 windows

## Summary

| Metric | Official CLI | Our Improved | Vanilla Baseline |
|--------|-------------|-------------|-----------------|
| Grounded | **8/15** | **6/15** | **8/15** |
| Terms found | 26/57 (46%) | 21/57 (37%) | 25/57 (44%) |
| Avg query | 19.1s | 13.9s | 23.8s |

---
### Query 1: Quote verbatim what Houston said to Columbia when Eagle landed at Tranquility Base.
**verbatim** | Verify: Tranquility, Eagle, landed

**Expected (transcript):**
```
05 03 10 32

Tape 79/10
Page 450
CDR
(TRANQ)

And, Houston, TranqUility
Base is going to give
you a few comments with regard to the geology
question of last night.
We are landed in a
relatively smooth crater field of elongate
secondary - circular secondary craters, most of
```

**Our Improved** (GROUNDED, 3/3 terms, 20.6s):
> Here’s the verbatim quote from Houston to Columbia when Eagle landed at Tranquility Base, as it appears in the provided transcript:

“**Columbia, this is Houston. Update? Over.**”

**Vanilla (no expansion)** (GROUNDED, 3/3 terms, 13.9s):
> Here’s the verbatim quote from Houston to Columbia when Eagle landed at Tranquility Base, as found in the provided transcript:

“We’re reading 67/6, 332 about it going?”

**Upstream Original** (GROUNDED, 3/3 terms, 26.3s):
> Here’s the verbatim quote from Houston to Columbia when Eagle landed at Tranquility Base, as extracted from the provided transcript:

“Okay. We've completed the uplink; the computer is yours. You can go BLOCK; however, we'd like you to hold off on the P52 option 1 align until after you've passed landing site 2; and we're requesting that you perform another P22 and attempt to find the I24 this pass

---
### Query 2: What did the astronauts describe about the color of the lunar surface? Quote their exact words.
**verbatim** | Verify: gray, chalky, basalt, Sun angle

**Expected (transcript):**
```
04 07 12 44

CDR
(TRANQ)

I'd say the color of the - The local surface is
very comparable to that we observed from orbit
at this Sun angle, about l0 degrees Sun angle,
or that nature.
It's pretty much without color.
It's gray, and it's a very white, chalky gray,
as you look into the zero-phase line; smd it's
considerably
darker gray, more like a ash ashen gray as you look out 90 degrees to thc S_m
```

**Our Improved** (WEAK, 1/4 terms, 19.1s):
> Here’s the exact quote from the astronaut describing the color of the lunar surface:

“As I look around the area, the contrast, in general, is *** comes about completely by virtue of the shadow *** down Sun ... very light-colored gray, light gray color, a halo around my own shadow, around the shadow of my helmet. Then, as I look off across *** the contrast becomes strongest in that the surromlding

**Vanilla (no expansion)** (WEAK, 1/4 terms, 14.4s):
> Here’s a quote of the astronaut’s description of the lunar surface color, based on the provided text:

“very light-colored gray, light gray color, a halo around my own shadow, around the shadow of my helmet. Then, as I look off across *** the contrast becomes strongest in that the surromlding color is still fairly light. As you look down into the Sun *** a larger amount of *** shadowed area is loo

**Upstream Original** (WEAK, 1/4 terms, 24.3s):
> Here’s the astronaut’s description of the lunar surface color, directly quoted from the text:

“As I look around the area, the contrast, in general, is *** comes about completely by virtue of the shadow *** down Sun ... very light-colored gray, light gray color, a halo around my own shadow, around the shadow of my helmet. Then, as I look off across *** the contrast becomes strongest in that the su

---
### Query 3: Quote verbatim the last goodnight message from Houston to the crew.
**verbatim** | Verify: good night, put you to bed, crew status

**Expected (transcript):**
```
CMP

Roger.

07 13 57 42

CC

Hello, Apollo 11. Houston.
We're read M to put
you to bed and say good night, if you give us
your crew status report and verify that you

Infinity.
```

**Our Improved** (WEAK, 0/3 terms, 19.1s):
> “Good evening. I’d like to discuss with you a few of the more symbolic aspects of the flight of our mission, Apollo 11. As we’ve been discussing the events that have taken place in the past 2 or 3 days here on board our spacecraft, we’ve come to the conclusion that this has been far more than three men on a voyage to the Moon; more, still, than the efforts of a government and industry team; more, 

**Vanilla (no expansion)** (WEAK, 0/3 terms, 15.0s):
> “There’s more moisture in the tunnel now than there has been at any previous time. Subjectively we have been unable to determine any change in humidity buildup in the tunnel. There appears to be no moisture anywhere else in the spacecraft. For example, the windows are not fogging or – and various other cool spots around the spacecraft – all of them appear to be completely dry.”

**Upstream Original** (WEAK, 0/3 terms, 22.9s):
> Here’s the verbatim last goodnight message from Houston to the crew, as extracted from the provided text:

“01 06 28 0”

“There’s more moisture in the tunnel now than there has been at Im3’ previous time. Subjectively we have been unable to determine any change in - Im3’ buildup in humidity. There appears to be no moisture anywhere else in the spacecraft. For example, the windows are not fogging o

---
### Query 4: What did the crew say about the chinch bugs? Quote the exact words.
**verbatim** | Verify: chinch bugs, mower, taciturn

**Expected (transcript):**
```
job, but I'll look into that for you.
07 05 39 51

_

Well,

he'll

tell you.

He's got a new mower.

07 05 39 53
```

**Our Improved** (GROUNDED, 2/3 terms, 19.4s):
> Here’s the exact quote from the transcript about the chinch bugs:

“Well, they’re sort of taciturn little fellows. They don’t say much; they just chomp away.”

**Vanilla (no expansion)** (WEAK, 1/3 terms, 13.9s):
> Here’s the requested quote from the transcript:

“Well, they’re sort of taciturn little fellows. They don’t say much; they just chomp away.”

**Upstream Original** (GROUNDED, 2/3 terms, 22.8s):
> Here’s the exact quote from the transcript about the chinch bugs:

“Well, they’re sort of taciturn little fellows. They don’t say much; they just chomp away.”

---
### Query 5: What was the astronauts' impression of the lunar soil from the core tube samples? Quote their exact words.
**verbatim** | Verify: core tube, moist, packed

**Expected (transcript):**
```
LMP
(TRANQ)

Yes.
That's about it.
It wasn't a rapid change
in resistive force.
And also I noticed when I
took the bit off that the material was quite
well packed, a good bit darker, and it - The way
it adhered to the core tube gave me the distinct
impression of being moist.
Over.
```

**Our Improved** (GROUNDED, 2/3 terms, 19.4s):
> Okay, let’s extract the relevant information from the provided transcript regarding the astronauts’ impression of the lunar soil from the core tube samples.

Here’s the quote from CDR Neil Armstrong:

“Well, I could do it like this, Owen. About all the struts are about equally stroked, and the height from the ground to the first step is about 3 feet or maybe 3 and 1/2 feet, huh?”

**Important Note

**Vanilla (no expansion)** (GROUNDED, 3/3 terms, 14.1s):
> Here’s the astronaut’s impression of the lunar soil from the core tube samples, based on the provided text:

“The material was quite well packed, a good bit darker, and it - The way it adhered to the core tube gave me the distinct impression of being moist.”

**Upstream Original** (WEAK, 1/3 terms, 22.8s):
> Okay, let’s break down the provided transcript and answer your question about the astronauts’ impression of the lunar soil.

**The Relevant Quote:**

The key quote is from CDR Neil Armstrong: “They're all looking wet. Houston, were you able to record the documentary way where the two core tube samples were taken? Negative. I didn't get a stereopair are right in the vicinity. Neil.”

**Astronauts’ 

---
### Query 6: What news stories from Earth were read to the astronauts? Quote the stories about Mrs. Goddard and the London bookie.
**factual** | Verify: crime-free, Goddard, London, bookie

**Expected (transcript):**
```
have shouted or anything.
He would just have
glowed."
She added, "That was his dream, sending a rocket to the Moon."
People around the
world had many reasons to be happy about the
Apollo ll mission.
The Italian police reported
that Sunday night was the most crime-free night
of the year.
And in London, a boy who had the
faith to bet $5 with a bookie that a man would
reach the Moon before 1970 colle
```

**Our Improved** (GROUNDED, 4/4 terms, 18.9s):
> Here’s a breakdown of the news stories read to the astronauts, based on the provided text:

*   **Mrs. Robert Goddard:** “Mrs. Robert Goddard said today that her husband would have been so happy. ‘He wouldn’t have shouted or anything. He would just have glowed.’ She added, ‘That was his dream, sending a rocket to the Moon.’”

*   **London Bookie:** “The Italian police reported that Sunday night wa

**Vanilla (no expansion)** (GROUNDED, 3/4 terms, 13.8s):
> Here are the news stories about Earth read to the astronauts, with the quoted sections:

*   **Mrs. Robert Goddard:** “She wouldn't have shouted or anything. She would just have glowed.” and “That was his dream, sending a rocket to the Moon.”

*   **The London Bookie:** “And in London, a boy who had the faith to bet $5 with a bookie that a man would reach the Moon before 1970 collected $2h 000. Th

**Upstream Original** (GROUNDED, 3/4 terms, 23.4s):
> Here are the news stories about Mrs. Robert Goddard and the London bookie as read to the astronauts:

*   **Mrs. Robert Goddard:** “States in the cause of peace.” And Mrs. Robert Goddard said today that her husband would have been so happy. “He wouldn't have shouted or anything. He would just have glowed.” She added, “That was his dream, sending a rocket to the Moon.”

*   **London Bookie:** “And 

---
### Query 7: What technical problems did the crew report about equipment that unfolded unevenly on the lunar surface?
**factual** | Verify: unfolded, unevenly, terrain, indentation

**Expected (transcript):**
```
.
0}4 18 40 19

LMP
(TRANQ)

I think that two corners did touch, since when it
was deployed, both of them didn't come out at the
same time.
It unfolded a little unevenly, and of
course, the terrain that it was on was a little
bit - not quite as level as it was - as I would
like to have it.
```

**Our Improved** (GROUNDED, 3/4 terms, 14.3s):
> According to the transcript, the crew reported the following technical problems with the equipment:

*   **Uneven unfolding:** The equipment unfolded unevenly.
*   **Uneven terrain:** The terrain was not as level as desired.
*   **Touching corners:** Two corners touched the lunar surface to a depth of about three-quarters to a half an inch.
*   **Triangular coating:** A small triangular coating wa

**Vanilla (no expansion)** (GROUNDED, 3/4 terms, 13.5s):
> According to the transcript, the crew reported the following technical problems with the equipment:

*   **Uneven unfolding:** The equipment unfolded unevenly.
*   **Uneven terrain:** The terrain was not as level as desired.
*   **Touching corners:** Two corners touched the lunar surface to a depth of about three-quarters to a half an inch.
*   **Triangular coating:** A small triangular coating wa

**Upstream Original** (GROUNDED, 2/4 terms, 23.2s):
> According to the transcript, the crew reported the following technical problems with the touch-down gear:

*   **Uneven Unfolding:** The touch-down gear unfolded unevenly.
*   **Corner Contact:** Two corners touched the lunar surface about three-quarters to a half an inch deep.
*   **Triangular Coating:** A small triangular coating of material (approximately 3 inches) was left on two of the corner

---
### Query 8: Quote the astronauts' farewell message where they said God bless you and good night from Apollo 11.
**verbatim** | Verify: Saturn, Columbia, Eagle, God bless

**Expected (transcript):**
```
The responsibility
for this flight lies first
with history and with the giants of science who
have preceded this effort; next with the American
people, who have thr<,ugh their will, indicated
their desire; next, _ o four administrations,
and
their Congresses,
fol' implementing that will;
and then, to the agel_cy and industry teams that
built our spacecraft_ the Saturn, the Columbia,
the Eagle, and
```

**Our Improved** (WEAK, 1/4 terms, 19.0s):
> Here’s the quote from the astronauts’ farewell message:

“People, tonight, we give a special thank you, and to all the other people that are listening and watching tonight, God bless you. Good night from Apollo 11.”

**Vanilla (no expansion)** (WEAK, 1/4 terms, 13.6s):
> “People, tonight, we give a special thank you, and to all the other people that are listening and watching tonight, God bless you. Good night from Apollo 11.”

**Upstream Original** (WEAK, 0/4 terms, 24.4s):
> Okay, here's a breakdown of the transcript, organized for clarity and highlighting key information:

**Tape 114/5 – Initial Communications & Stowage**

*   **07 09 43 52 - 07 09 47 48:**  Initial greetings and a request from Apollo 11 to crank up the PTC (Panoramic Telescope Capability) for a TV broadcast.
*   **07 09 47 57 - 07 09 48 10:**  Houston confirms the PTC can be cranked up.  A comment a

---
### Query 9: What happened with the television camera on the lunar surface? Quote what Houston said about seeing the Eagle and Earth.
**factual** | Verify: TV, camera, focus, Earth, eagle

**Expected (transcript):**
```
01 10 29 23

CC

Apollo 11, Houston.
The color is better now.
It's coming in. We could attempt a little bit
better focus on it.
There we go; it focuses a
lot better now.
We see the eagle coming right
in on the lunar surface.
Over.
```

**Our Improved** (WEAK, 2/5 terms, 19.5s):
> Here’s a breakdown of what happened with the television camera on the lunar surface, as relayed in the provided transcript:

**The Setup:**

*   Apollo 11 was using a camera to zoom in on the lunar surface, aiming for the highest possible magnification.
*   Houston was monitoring the feed and describing what they were seeing.

**What They Saw:**

*   **Earth:** The camera showed a view of Earth, a

**Vanilla (no expansion)** (WEAK, 0/5 terms, 13.7s):
> Here’s the relevant quote from the transcript:

“The definition is pretty good on our monitor here. The color is not too ..., at least on this set. Could you describe what you’re looking at? Over.”

Houston then asks for a description of what Charlie is seeing.

























































































































**Upstream Original** (WEAK, 2/5 terms, 24.6s):
> Here’s a breakdown of what happened with the television camera on the lunar surface, as relayed in the provided transcript:

**The Setup:**

*   Apollo 11 was using a camera to zoom in on the lunar surface, aiming for the highest possible magnification.
*   Houston was monitoring the feed and describing what they were seeing.

**What They Saw:**

*   **Earth:** The camera showed a view of Earth, a

---
### Query 10: How did Neil describe collecting rock samples around the elongate double crater?
**factual** | Verify: rock, sample, crater, variety, exhaust

**Expected (transcript):**
```
ro(_kzl
Oll
th(,
surface,
and ucveral
that
weru JusL LiuL)_LII'I'i_C_ -about 20 - 15 to 20 feet north of the t/q. And
then I recalled that that area had been probably
swept pretty well by the exhaust of the descent
engine, so I crossed over to the southern side
of the IR, and took a number of samples from the
area around the elongate double crater that we
commented on, and several beyond that, and
```

**Our Improved** (GROUNDED, 3/5 terms, 16.9s):
> According to the transcript, Neil described collecting rock samples around the elongate double crater by:

*   Starting on the cut side of the LM that the TV camera was on.
*   Taking 15-20 feet north of the LM.
*   Crossing over to the southern side of the LM.
*   Taking a number of samples from the area around the elongate double crater and several beyond it.
*   Trying to collect as many differ

**Vanilla (no expansion)** (GROUNDED, 4/5 terms, 13.5s):
> According to Neil, he initially started collecting samples from the cut side of the LM (Lunar Module) where the TV camera was located. He then moved to the southern side of the LM to avoid the exhaust from the descent engine and collected samples around the elongate double crater and several others beyond it, trying to gather as many different types of rock as possible within the limited time avai

**Upstream Original** (GROUNDED, 3/5 terms, 23.7s):
> Neil described collecting rock samples around the elongate double crater by:

*   Taking a number of samples from the area around the crater and several beyond it.
*   Trying to take as many different types of rock types as he could see by eye in the short time available.
*   He noted he collected samples from the cut side of the LM that the TV camera was on, about 20-15 to 20 feet north of the TV

---
### Query 11: What was said at mission time 04 06 46 04? Quote the exact words from the transcript at that timestamp.
**timestamp** | Verify: Eagle, Tranquility, landed, copy you down

**Expected (transcript):**
```
CC

We copy you down,

CDR
(TRA_Q)

Houston,

CDR

THE EAGLE

Eagle.
```

**Our Improved** (WEAK, 0/4 terms, 19.2s):
> The exact words from the transcript at mission time 04 06 46 04 were:

“Must be Okay.”

**Vanilla (no expansion)** (WEAK, 0/4 terms, 13.5s):
> At mission time 04:06:46:04, the transcript reads: “Okay. We’re all listening.”

**Upstream Original** (WEAK, 0/4 terms, 23.3s):
> The exact words from the transcript at mission time 04 06 46 04 are: “a phone call from San Francisco just before he boarded a plane to fly out to meet you.”

---
### Query 12: What happened at timestamp 04 13 23 38? What did the Commander report about the ladder and the surface?
**timestamp** | Verify: foot of the ladder, footpads, depressed, powder, fine grained

**Expected (transcript):**
```
04 13 23 38

CDR
(TRANQ)

I'm at the foot of the ladder.
The I2! footpads
are only depressed in the surface about I or
2 inches, although the surface appears to be very,
very fine grained, as you get close te it.
It's
almost like a powder.
Down-there,
it's very fine.
```

**Our Improved** (WEAK, 0/5 terms, 19.7s):
> At timestamp 04 13 23 38, the Commander reported that “Our monitor shows pretty good, clear pictures from this angle. I already found the 90-degree bracket.” He was observing the view through the window via the ACA system.

**Vanilla (no expansion)** (WEAK, 0/5 terms, 13.6s):
> At timestamp 04 13 23 38, the Commander (CDR) reported that “Our monitor shows pretty good, clear pictures from this angle.” He had already found the 90-degree bracket and was commenting on the quality of the images being received.


**Upstream Original** (GROUNDED, 3/5 terms, 23.8s):
> At timestamp 04 13 23 38, the Commander (CDR) reported the following about the ladder and the surface:

*   The I2 footpads were only depressed about 1 or 2 inches into the surface.
*   The surface appeared very fine-grained, almost like a powder.
*   When he got close to the surface, it felt like powdered charcoal, adhering to his boots.
*   He was only able to step into the surface a small fract

---
### Query 13: At mission time 04 14 16 09, who called the astronauts and what was announced?
**timestamp** | Verify: President, United States, office, few words

**Expected (transcript):**
```
Roger.
We'd like to get both of you in the field
of view of the camera for a minute.

04 14 16 09

CC

Neil and Buzz, the President of the U_oited States
is in his office now and would like to say a
few words to you.
Over.
```

**Our Improved** (GROUNDED, 2/4 terms, 20.2s):
> Okay, let's break down the transcript to answer your question.

**Who called the astronauts and what was announced?**

The President of the United States, Richard M. Nixon, called the astronauts (Neil and Buzz Aldrin) at mission time 04 14 16 23.

He announced that he was speaking to them from the Oval Room at the White House and that this was “the most historic telephone clipping of words and phr

**Vanilla (no expansion)** (WEAK, 0/4 terms, 13.9s):
> Okay, let's break down the text to find the answer to your question.

According to the text, at mission time 04 14 16 09, **CDR (Command and Data Recorder)** called the astronauts. 

What was announced is: **"Okay. We're all listening."**



**Upstream Original** (WEAK, 0/4 terms, 23.7s):
> At mission time 04 14 16 09, Bruce called the astronauts and announced the following:

*   “We're all listening.”
*   “Okay.”
*   “Roger.”
*   “Roger.”
*   “And I understand he was down there and really enjoyed watching the launch. We all think it was pretty magnificent, and you all are doing a great job up there.”
*   “Thank you.”

The tape also includes a quote from the astronauts themselves, Ne

---
### Query 14: What did Buzz say at timestamp 07 05 39 34 about his lawn? Quote the exact exchange.
**timestamp** | Verify: lawn, cut, mower, Buzz

**Expected (transcript):**
```
112/3
578

07 05 39 34

_MI_

That was Nell.
This is Buzz, here.
I wi:;h
we could find out when the last time my lawn
was cut.
Over.
```

**Our Improved** (GROUNDED, 3/4 terms, 20.4s):
> Here’s the exact exchange from timestamp 07 05 39 34:

“That was Nell. This is Buzz, here. I wish we could find out when the last time my lawn was cut. Over.”

**Vanilla (no expansion)** (GROUNDED, 2/4 terms, 13.5s):
> The provided text does not contain any information about Buzz's lawn. It focuses on a conversation between Apollo 11 and Houston during a space mission.

**Upstream Original** (GROUNDED, 3/4 terms, 23.6s):
> “That was Nell. This is Buzz, here. I wish we could find out when the last time my lawn was cut. Over.”

---
### Query 15: What communication happened at timestamp 08 03 15 03 near the end of the mission? Who was talking to Apollo 11?
**timestamp** | Verify: Hornet, Apollo 11

**Expected (transcript):**
```
15.

11.

This

is Hornet.

Hornet.

This is Apollo 11 read:ng you
Our position 1330, 16_ 15.
```

**Our Improved** (WEAK, 0/2 terms, 20.0s):
> At timestamp 08 03 15 03 near the end of the mission, Neil Armstrong (CDR Tranquility) was communicating with Houston. He was requesting the fixed portion of the ascent pad to be loaded in for a specific purpose.




**Vanilla (no expansion)** (WEAK, 0/2 terms, 14.4s):
> At timestamp 04 14 38 27, Houston contacted Columbia. The message included "LOS will be aw, !11 19 31; AOS, 1!2 05 4_. Over."

There is no communication recorded at timestamp 08 03 15 03 near the end of the mission.

**Upstream Original** (GROUNDED, 2/2 terms, 24.2s):
> Okay, let's break down the communication happening at timestamp 08 03 15 03 near the end of the mission, based on the provided transcript excerpts.

**Who was talking to Apollo 11?**

The communication at 08 03 15 03 was between **President Nixon** and the crew of Apollo 11 (LMP - Neil Armstrong, and CMP - Buzz Aldrin).

**What communication happened?**

The excerpt describes the following:

*   *
