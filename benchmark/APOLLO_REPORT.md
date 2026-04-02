# Apollo 11 Transcript RAG Benchmark

**Generated:** 2026-04-02T08:04:49.858789
**Model:** `gemma-3-4b-it`
**Document:** 370,778 tokens | 725 windows | Markov boundary reconstruction
**Store:** 725 windows, 8,159 entries, 11,450 IDF tokens

## Summary

| Metric | Value |
|--------|-------|
| Queries grounded | **3/10 (30%)** |
| Verification terms found | 9/35 (26%) |
| Avg query time | 43790ms |
| Model load time | 5.1s |

### By Category

- **Verbatim:** 1/5
- **Factual:** 2/4
- **Interpretive:** 0/1

## Query Results

| # | Category | Grounded | Terms | Time (ms) | Query |
|---|----------|----------|-------|-----------|-------|
| 1 | verbatim | weak | 0/3 | 37745 | Quote verbatim what Houston said to Columbia when Eagle land... |
| 2 | verbatim | weak | 1/4 | 34579 | What did the astronauts describe seeing on the lunar surface... |
| 3 | verbatim | weak | 0/3 | 32772 | Quote verbatim the goodnight message from Houston near the e... |
| 4 | verbatim | yes | 1/2 | 46997 | What did the crew say about the chinch bugs? Quote the exact... |
| 5 | verbatim | weak | 1/3 | 74459 | What was the astronauts' impression of the lunar soil when t... |
| 6 | factual | weak | 0/4 | 45177 | What news from Earth was read to the astronauts during the m... |
| 7 | factual | weak | 0/3 | 42543 | What technical problems did the crew report during their EVA... |
| 8 | interpretive | weak | 0/5 | 41584 | Describe the astronauts' closing remarks before splashdown. ... |
| 9 | factual | yes | 2/4 | 42233 | What was the crew's experience with the television broadcast... |
| 10 | factual | yes | 4/4 | 39810 | How did the crew describe the process of collecting rock sam... |

## Timing Breakdown

| # | Expansion (ms) | Route (ms) | Prefill (ms) | Generate (ms) | Total (ms) |
|---|---------------|------------|-------------|--------------|------------|
| 1 | 1488 | 18 | 7325 | 27409 | 37745 |
| 2 | 1255 | 8 | 5996 | 26036 | 34579 |
| 3 | 1314 | 7 | 5875 | 24217 | 32772 |
| 4 | 1339 | 4 | 7445 | 36813 | 46997 |
| 5 | 1624 | 29 | 17188 | 53853 | 74459 |
| 6 | 1875 | 28 | 10290 | 31005 | 45177 |
| 7 | 1514 | 21 | 8835 | 29513 | 42543 |
| 8 | 2125 | 48 | 8117 | 28940 | 41584 |
| 9 | 1528 | 8 | 9145 | 29894 | 42233 |
| 10 | 2065 | 35 | 7792 | 27643 | 39810 |

## Full Query Outputs

### Query 1: Quote verbatim what Houston said to Columbia when Eagle landed. Provide only the exact words from the transcript.
- **Category:** verbatim | **Windows:** [354, 532, 558]
- **Verification:** 0/3 terms found
  - Found: (none)
  - Missing: Tranquility Base, Eagle, landed
- **Output:**

> “We'll have AOS for you 102 16.”

### Query 2: What did the astronauts describe seeing on the lunar surface? Quote their exact words about the color and texture.
- **Category:** verbatim | **Windows:** [466, 465, 76]
- **Verification:** 1/4 terms found
  - Found: gray
  - Missing: chalky, basalt, Sun angle
- **Output:**

> Here’s a breakdown of what the astronauts described seeing on the lunar surface, based on the provided transcript:
> 
> *   **Color:** “very light-colored gray, light gray color, a halo around my own shadow, around the shadow of my helmet.” “ash-cocoa color.” “the blue color of my boots has completely disappeared now into this ash-cocoa color.”
> 
> *   **Texture:** “considerably darker in texture.” “It seems to be covering most of the lighter part of the boots *** very fine particles.”

### Query 3: Quote verbatim the goodnight message from Houston near the end of the mission.
- **Category:** verbatim | **Windows:** [373, 502, 129]
- **Verification:** 0/3 terms found
  - Found: (none)
  - Missing: good night, bed, crew status
- **Output:**

> “Goodnight Base, again. this is Houston. Go ahead.”

### Query 4: What did the crew say about the chinch bugs? Quote the exact exchange from the transcript.
- **Category:** verbatim | **Windows:** [673, 682, 493]
- **Verification:** 1/2 terms found
  - Found: chinch bugs
  - Missing: mower
- **Output:**

> Okay, let's extract the exact exchange about the chinch bugs from the transcript:
> 
> **CMP:** “Well, they’re sort of taciturn little fellows. They don’t say much; they just chomp away.”
> 
> **CC:** “Concur on that.”
> 
> Let me know if you’d like me to find any other specific quotes or information from the transcript!

### Query 5: What was the astronauts' impression of the lunar soil when they collected core tube samples? Quote their exact words.
- **Category:** verbatim | **Windows:** [508, 505, 478]
- **Verification:** 1/3 terms found
  - Found: moist
  - Missing: core tube, packed
- **Output:**

> Here’s the relevant excerpt from the transcript, quoting the astronauts’ impressions of the lunar soil:
> 
> “want to stay vertical, that they'd tend
> to fall over on you even after pounding in that
> far. Is that correct?”
> 
> “The ones that I saw back in the aft end of the
> spacecraft appeared to be a good bit darker; of
> course, viewed from the aft end, why, they did
> have the Sun shining directly on them.
> It seemed
> as though the material had been baked somewhat and
> also scattered in a radially outward direction,
> but in
> 
> ---
> 
> 15 18
> 
> Oh
> 
> L4
> 
> I',18 3'{
> 
> 0}l 15 18 51
> 
> CC
> 
> CMP
> (COLUMBIA)
> 
> looks wet.
> 
> While I'm getting the next one, maybe
> can - ... away the box a little bit.
> 
> you
> 
> Understand.
> 
> Columbia.
> 
> is Hot_ston.
> 
> Approximat_.ly
> 
> 1 minute
> 
> Roger.
> 
> And, do you plan on commencing your sleep on the
> backside this pass?
> If so, we'll disable uplink
> bo you while we're talking to the laM. Over.
> Negative
> 
> that.”
> 
> **Regarding the question about the astronauts' impression of the lunar soil:**
> 
> The most direct quote is from LMP (James Lovell) describing the soil as "a good bit darker."  He also notes it "had been baked somewhat and also scattered in a radially outward direction."
> 
> There's also a brief mention of it "looking wet" from the aft end of the spacecraft, which suggests a moist or damp texture.

### Query 6: What news from Earth was read to the astronauts during the mission? Quote the specific stories mentioned.
- **Category:** factual | **Windows:** [76, 704, 588]
- **Verification:** 0/4 terms found
  - Found: (none)
  - Missing: crime-free, Goddard, London, bookie
- **Output:**

> Okay, here’s a breakdown of the news stories read to the Apollo 11 astronauts during the mission, as transcribed from the provided text:
> 
> 1.  **Soviet Moon Mission Failure:** “Britain's big Jodrell Bank radio telescope stopped receiving signals from the Soviet Union’s unmanned Moon shot at 5:49 EDT today. A spokesman said that it appeared the Luna 15 space ship “had gone beyond the Moon.””
> 
> 2.  **Mars Mission Proposal:** “Vice President Spiro T. Agnew has called for putting a man on Mars by the year 2000, but Democratic leaders replied that priority must go to needs on Earth.”
> 
> 3.  **Hippy Restrictions in Mexico:** “Immigration officials in Nuevo Laredo announced hippies will be refused tourist cards to enter Mexico unless they take a bath and get haircuts.”
> 
> 4.  **Apollo II Reaction Globally:** “Europe is Moon-struck by the Apollo ll mission. Newspapers throughout the continent fill their pages with pictures of the Saturn V rocket blasting off to forge Earth’s first link with its natural satellite. And the headline writers taxed their imagination for words to hail the feat.”
> 
> 5.  **Intelsat Launch Delay:** “The launch of Intelsat from the Cape was postponed for the fourth time last night. The problem was said to be a malfunctioning nitrogen regulator in the second stage of Delta. A new attempt will be made to launch it tonight.”
> 
> 6.  **Ben Franklin Submarine Record:** “The research submarine Ben Franklin, which is studying the Gulf Stream, set a record by drifting 24 hours from 10 to 100 feet above the ocean floor in 1300 feet of water off the Georgia coast.”
> 
> 7.  **Wally Schirra’s Election:** “Wally Schirra has been elected to a 5-year term on the board of trustees of the Detroit Institute of Technology.”
> 
> 8.  **Air Canada Moon Flights:** “Air Canada says it has accepted 2300 reservations for flights to the Moon in the past 5 days. It might be noted that more than 100 have been made by men for their mothers-in-law.”
> 
> 9.  **Moon Song Phenomenon:** “Nashville, Tennessee, which probably houses the largest collection of recording companies and song publishers in the country, now reports it is

### Query 7: What technical problems did the crew report during their EVA on the lunar surface?
- **Category:** factual | **Windows:** [69, 461, 74]
- **Verification:** 0/3 terms found
  - Found: (none)
  - Missing: unfolded, unevenly, terrain
- **Output:**

> According to the transcript, the crew reported that the gas separators on the water were leaking at the junction between the food bag and the water filter.

### Query 8: Describe the astronauts' closing remarks before splashdown. What did they thank people for?
- **Category:** interpretive | **Windows:** [462, 616, 614]
- **Verification:** 0/5 terms found
  - Found: (none)
  - Missing: spacecraft, Saturn, Columbia, Eagle, God bless
- **Output:**

> Here’s a breakdown of the astronauts’ closing remarks before splashdown, based on the provided transcript:
> 
> **The Astronauts’ Closing Remarks:**
> 
> As the transcript ends, we hear Neil Armstrong and Buzz Aldrin speaking on the radio. Here’s what they said:
> 
> “Okay, Houston, Tranquility Base here. The overview and observations of the lunar surface are complete and we’re prepared to begin our ascent.”
> 
> “We’d like to take this opportunity to say that the U.S. President and the people of America are greatly appreciated for their support.”
> 
> **What they thanked people for:**
> 
> They expressed gratitude to the President and the people of America for their support of the mission. 
> 
> Let me know if you’d like me to extract any other specific details from the transcript!

### Query 9: What was the crew's experience with the television broadcast from the lunar surface?
- **Category:** factual | **Windows:** [627, 462, 236]
- **Verification:** 2/4 terms found
  - Found: TV, camera
  - Missing: focus, Earth
- **Output:**

> According to the transcript, the crew’s experience with the television broadcast from the lunar surface was overwhelmingly positive, with significant attention and coverage from around the world. Here’s a breakdown of the key points:
> 
> *   **Initial Observation:** Buzz Aldrin specifically noted a “very bright spot of light” and confirmed Neil Armstrong’s observation of its position.
> *   **Sample Selection Context:** The crew believed the selection of samples for the container was influenced by the rocks themselves, suggesting a careful and considered approach.
> *   **TV Camera Location:** Neil Armstrong initially set up the TV camera on the cut side of the LM, taking samples approximately 15-20 feet north of it. He then moved to the southern side to collect samples around the elongate double crater.
> *   **Variety of Samples:** They aimed to collect as many different types of rock as possible within the limited time.
> *   **Presidential Message:** The entire conversation was prompted by a phone call from President Nixon, who expressed immense pride in the astronauts’ achievement and acknowledged the global media attention.
> *   **Worldwide Coverage:** The transcript details extensive media coverage from the US (including "Apollo Day" declarations and TV installations) and internationally (West Germany, BBC, Italy, and even the Soviet Union – with a space engineer commenting on Luna 15’s capabilities).
> *   **Social Events:** The crew’s wives and children had a celebratory lunch, with the children engaging in activities at Buzz Aldrin’s house.
> 
> In essence, the mission was a global event, and the television broadcast was a central element of that phenomenon.

### Query 10: How did the crew describe the process of collecting rock samples on the Moon?
- **Category:** factual | **Windows:** [638, 637, 627]
- **Verification:** 4/4 terms found
  - Found: rock, sample, crater, variety
- **Output:**

> According to the transcript, the crew described the process of collecting rock samples as follows:
> 
> 1.  **Initial Sampling:** Neil initially started on the cut side of the LM where the TV camera was located and took samples from rocks about 20-20 feet north of the LM.
> 2.  **Exhaust Sweep:** He recognized that this area had been swept by the descent engine exhaust and moved to the southern side of the LM.
> 3.  **Around Crater:** From the southern side, he took samples around the elongate double crater.
> 4.  **Variety of Rock Types:** He tried to collect as many different types of rock as possible by eye within the limited time available.
