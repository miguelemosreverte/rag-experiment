# Apollo 11 Transcript RAG Benchmark

**Generated:** 2026-04-02T08:27:40.146435
**Model:** `gemma-3-4b-it`
**Routing:** `improved`
**Document:** 370,778 tokens | 725 windows | Markov boundary reconstruction

## Summary

| Metric | Value |
|--------|-------|
| Queries grounded | **6/10 (60%)** |
| Verification terms found | 20/38 (53%) |
| Avg query time | 42.8s |

## Query Results with Source Verification

### Query 1: Quote verbatim what Houston said to Columbia when Eagle landed at Tranquility Base.
**verbatim** | **GROUNDED** | Terms: 3/3 | Windows: [389, 487, 532] | 34.8s

Found: Tranquility, Eagle, landed

**Expected (from transcript):**
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

**Model output:**
> Here’s the verbatim quote from Houston to Columbia when Eagle landed at Tranquility Base, as it appears in the provided transcript:

“**Columbia, this is Houston. Update? Over.**”

---

### Query 2: What did the astronauts describe about the color of the lunar surface? Quote their exact words.
**verbatim** | **WEAK** | Terms: 1/4 | Windows: [76, 466, 263] | 34.7s

Found: gray
Missing: chalky, basalt, Sun angle

**Expected (from transcript):**
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
darker gray, more like a ash ashen gray as you look out 90 degrees to thc S_m.
```

**Model output:**
> Here’s the exact quote from the astronaut describing the color of the lunar surface:

“As I look around the area, the contrast, in general, is *** comes about completely by virtue of the shadow *** down Sun ... very light-colored gray, light gray color, a halo around my own shadow, around the shadow of my helmet. Then, as I look off across *** the contrast becomes strongest in that the surromlding color is still fairly light. As you look down into the Sun *** a larger amount of *** shadowed area

---

### Query 3: Quote verbatim the last goodnight message from Houston to the crew.
**verbatim** | **WEAK** | Terms: 0/3 | Windows: [678, 686, 589] | 35.2s

Missing: good night, put you to bed, crew status

**Expected (from transcript):**
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

**Model output:**
> “Good evening. I’d like to discuss with you a few of the more symbolic aspects of the flight of our mission, Apollo 11. As we’ve been discussing the events that have taken place in the past 2 or 3 days here on board our spacecraft, we’ve come to the conclusion that this has been far more than three men on a voyage to the Moon; more, still, than the efforts of a government and industry team; more, even, than the efforts of one nation. We feel that this stands as a symbol of the insatiable curiosi

---

### Query 4: What did the crew say about the chinch bugs? Quote the exact words.
**verbatim** | **GROUNDED** | Terms: 2/3 | Windows: [673, 682, 76] | 62.0s

Found: chinch bugs, taciturn
Missing: mower

**Expected (from transcript):**
```
Well,

he'll

tell you.

He's got a new mower.

07 05 39 53

CC

Roger.
```

**Model output:**
> Here’s the exact quote from the transcript about the chinch bugs:

“Well, they’re sort of taciturn little fellows. They don’t say much; they just chomp away.”

---

### Query 5: What was the astronauts' impression of the lunar soil from the core tube samples? Quote their exact words.
**verbatim** | **GROUNDED** | Terms: 2/3 | Windows: [508, 638, 478] | 83.3s

Found: core tube, packed
Missing: moist

**Expected (from transcript):**
```
04 18 4B 23

CC

Roger.
Understand the general impression of
being moist as it packed in the core tube.
Next
question:
we did copy your comments prior to
the EVA of your general description
of the area.
We wonder if either of you would have any more
```

**Model output:**
> Okay, let’s extract the relevant information from the provided transcript regarding the astronauts’ impression of the lunar soil from the core tube samples.

Here’s the quote from CDR Neil Armstrong:

“Well, I could do it like this, Owen. About all the struts are about equally stroked, and the height from the ground to the first step is about 3 feet or maybe 3 and 1/2 feet, huh?”

**Important Note:** This quote doesn't directly address the *soil* itself. It’s about the mechanical operation of a 

---

### Query 6: What news stories from Earth were read to the astronauts? Quote the stories about Mrs. Goddard and the London bookie.
**factual** | **GROUNDED** | Terms: 4/4 | Windows: [589, 76, 462] | 43.4s

Found: crime-free, Goddard, London, bookie

**Expected (from transcript):**
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
reach the Moon before 1970 collected $2h 000.
That's pretty good odds.
```

**Model output:**
> Here’s a breakdown of the news stories read to the astronauts, based on the provided text:

*   **Mrs. Robert Goddard:** “Mrs. Robert Goddard said today that her husband would have been so happy. ‘He wouldn’t have shouted or anything. He would just have glowed.’ She added, ‘That was his dream, sending a rocket to the Moon.’”

*   **London Bookie:** “The Italian police reported that Sunday night was the most crime-free night of the year. And in London, a boy who had the faith to bet $5 with a boo

---

### Query 7: What technical problems did the crew report about equipment that unfolded unevenly on the lunar surface?
**factual** | **GROUNDED** | Terms: 3/4 | Windows: [507] | 29.9s

Found: unfolded, unevenly, terrain
Missing: indentation

**Expected (from transcript):**
```
LMP
(TRANQ)

I think that two corners did touch, since when it
was deployed, both of them didn't come out at the
same time.
It unfolded a little unevenly, and of
course, the terrain that it was on was a little
bit - not quite as level as it was - as I would
like to have it.
And I think that two corners
did touch to about i inch - no, three-quarters
to a half an inch deep; and maybe along the bottom,
```

**Model output:**
> According to the transcript, the crew reported the following technical problems with the equipment:

*   **Uneven unfolding:** The equipment unfolded unevenly.
*   **Uneven terrain:** The terrain was not as level as desired.
*   **Touching corners:** Two corners touched the lunar surface to a depth of about three-quarters to a half an inch.
*   **Triangular coating:** A small triangular coating was left on two of the corners, likely due to the corners digging into the surface.
*   **Difficulty p

---

### Query 8: Quote the astronauts' closing remarks where they thanked the people who built the spacecraft, mentioning Saturn, Columbia, and Eagle.
**verbatim** | **WEAK** | Terms: 0/4 | Windows: [616, 687] | 32.4s

Missing: Saturn, Columbia, Eagle, God bless

**Expected (from transcript):**
```
Out.

04 01 17 08

CC

Columbia and Eagle:
LOS for both
97 32, AOS 98 18.
Houston, out.

END OF TAPE
```

**Model output:**
> “We would like to give a special thanks to all those Americans who built the spacecraft, who aided the construction, design, the tests, and put their – their hearts and all their abilities into those crafts. To those…”

---

### Query 9: What happened with the television camera on the lunar surface? Quote what Houston said about seeing the Eagle and Earth.
**factual** | **WEAK** | Terms: 2/5 | Windows: [128, 76, 627] | 38.6s

Found: camera, Earth
Missing: TV, focus, eagle

**Expected (from transcript):**
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

**Model output:**
> Here’s a breakdown of what happened with the television camera on the lunar surface, as relayed in the provided transcript:

**The Setup:**

*   Apollo 11 was using a camera to zoom in on the lunar surface, aiming for the highest possible magnification.
*   Houston was monitoring the feed and describing what they were seeing.

**What They Saw:**

*   **Earth:** The camera showed a view of Earth, appearing as a “little more than a half Earth” to the left of the LM (Lunar Module).
*   **North Amer

---

### Query 10: How did Neil describe collecting rock samples around the elongate double crater?
**factual** | **GROUNDED** | Terms: 3/5 | Windows: [627, 532] | 34.2s

Found: rock, sample, crater
Missing: variety, exhaust

**Expected (from transcript):**
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
commented on, and several beyond that, and tried
to take as many different types - of rock types
```

**Model output:**
> According to the transcript, Neil described collecting rock samples around the elongate double crater by:

*   Starting on the cut side of the LM that the TV camera was on.
*   Taking 15-20 feet north of the LM.
*   Crossing over to the southern side of the LM.
*   Taking a number of samples from the area around the elongate double crater and several beyond it.
*   Trying to collect as many different types of rock as he could see by eye in the short time available.

---
