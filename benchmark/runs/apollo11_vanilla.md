# Apollo 11 Transcript RAG Benchmark

**Generated:** 2026-04-02T08:34:53.265801
**Model:** `gemma-3-4b-it`
**Routing:** `vanilla`
**Document:** 370,778 tokens | 725 windows | Markov boundary reconstruction

## Summary

| Metric | Value |
|--------|-------|
| Queries grounded | **5/10 (50%)** |
| Verification terms found | 18/38 (47%) |
| Avg query time | 27.8s |

## Query Results with Source Verification

### Query 1: Quote verbatim what Houston said to Columbia when Eagle landed at Tranquility Base.
**verbatim** | **GROUNDED** | Terms: 3/3 | Windows: [389] | 26.6s

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
> Here’s the verbatim quote from Houston to Columbia when Eagle landed at Tranquility Base, as found in the provided transcript:

“We’re reading 67/6, 332 about it going?”

---

### Query 2: What did the astronauts describe about the color of the lunar surface? Quote their exact words.
**verbatim** | **WEAK** | Terms: 1/4 | Windows: [466] | 26.0s

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
> Here’s a quote of the astronaut’s description of the lunar surface color, based on the provided text:

“very light-colored gray, light gray color, a halo around my own shadow, around the shadow of my helmet. Then, as I look off across *** the contrast becomes strongest in that the surromlding color is still fairly light. As you look down into the Sun *** a larger amount of *** shadowed area is looking toward us. The general color of the *** surrounding *** the contrast is not as great. Surveying

---

### Query 3: Quote verbatim the last goodnight message from Houston to the crew.
**verbatim** | **WEAK** | Terms: 0/3 | Windows: [678] | 26.3s

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
> “There’s more moisture in the tunnel now than there has been at any previous time. Subjectively we have been unable to determine any change in humidity buildup in the tunnel. There appears to be no moisture anywhere else in the spacecraft. For example, the windows are not fogging or – and various other cool spots around the spacecraft – all of them appear to be completely dry.”

---

### Query 4: What did the crew say about the chinch bugs? Quote the exact words.
**verbatim** | **WEAK** | Terms: 1/3 | Windows: [673] | 26.3s

Found: taciturn
Missing: chinch bugs, mower

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
> Here’s the requested quote from the transcript:

“Well, they’re sort of taciturn little fellows. They don’t say much; they just chomp away.”

---

### Query 5: What was the astronauts' impression of the lunar soil from the core tube samples? Quote their exact words.
**verbatim** | **GROUNDED** | Terms: 3/3 | Windows: [508] | 24.8s

Found: core tube, moist, packed

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
> Here’s the astronaut’s impression of the lunar soil from the core tube samples, based on the provided text:

“The material was quite well packed, a good bit darker, and it - The way it adhered to the core tube gave me the distinct impression of being moist.”

---

### Query 6: What news stories from Earth were read to the astronauts? Quote the stories about Mrs. Goddard and the London bookie.
**factual** | **GROUNDED** | Terms: 3/4 | Windows: [589] | 25.2s

Found: Goddard, London, bookie
Missing: crime-free

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
> Here are the news stories about Earth read to the astronauts, with the quoted sections:

*   **Mrs. Robert Goddard:** “She wouldn't have shouted or anything. She would just have glowed.” and “That was his dream, sending a rocket to the Moon.”

*   **The London Bookie:** “And in London, a boy who had the faith to bet $5 with a bookie that a man would reach the Moon before 1970 collected $2h 000. That's pretty good odds.”

---

### Query 7: What technical problems did the crew report about equipment that unfolded unevenly on the lunar surface?
**factual** | **GROUNDED** | Terms: 3/4 | Windows: [507] | 25.7s

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
**verbatim** | **WEAK** | Terms: 0/4 | Windows: [687] | 23.5s

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
> “We would like to give a special thanks to all those Americans who built the spacecraft, who aided the construction, design, the tests, and put their – their hearts and all their abilities into those crafts.”

---

### Query 9: What happened with the television camera on the lunar surface? Quote what Houston said about seeing the Eagle and Earth.
**factual** | **WEAK** | Terms: 0/5 | Windows: [128] | 24.5s

Missing: TV, camera, focus, Earth, eagle

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
> Here’s the relevant quote from the transcript:

“The definition is pretty good on our monitor here. The color is not too ..., at least on this set. Could you describe what you’re looking at? Over.”

Houston then asks for a description of what Charlie is seeing.





























































































































































































































---

### Query 10: How did Neil describe collecting rock samples around the elongate double crater?
**factual** | **GROUNDED** | Terms: 4/5 | Windows: [627] | 49.1s

Found: rock, sample, crater, exhaust
Missing: variety

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
> According to Neil, he initially started collecting samples from the cut side of the LM (Lunar Module) where the TV camera was located. He then moved to the southern side of the LM to avoid the exhaust from the descent engine and collected samples around the elongate double crater and several others beyond it, trying to gather as many different types of rock as possible within the limited time available.

---
