# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0** — A tier-weighted content-based music recommender.

---

## 2. Intended Use

This system suggests the top 3–5 songs from a small catalog based on a user's preferred genre, mood, energy level, and optional audio features. It is designed for classroom exploration in CodePath AI110, not for real users or production deployment. It assumes the user can articulate their taste as a set of feature preferences.

---

## 3. How the Model Works

The system compares every song in the catalog to a user's taste profile. Each song feature (genre, mood, energy, etc.) is checked for similarity: categorical features like genre are either a match or not, while numeric features like energy get a percentage score based on how close the values are.

Not all features are treated equally. The system uses a three-tier weighting system:
- **Tier 1** (genre, mood, energy) — the "vibe" features — get the highest weight because they define how music *feels*.
- **Tier 2** (acousticness, valence) — supporting features that add nuance.
- **Tier 3** (danceability, tempo) — tiebreakers that rarely change the ranking on their own.

Each song gets a final score between 0 and 1. The songs are sorted highest to lowest, and the top results are returned with a plain-English explanation of why they were chosen.

---

## 4. Data

- **18 songs** in `data/songs.csv` (10 original + 8 added for genre diversity)
- **15 genres**: pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, electronic, r&b, metal, bossa nova, chiptune, folk, house
- **12 moods**: happy, chill, intense, relaxed, focused, moody, nostalgic, energetic, romantic, aggressive, playful, melancholy
- The original 10 songs skewed toward pop and lofi. The 8 added songs were chosen specifically to fill genre/mood gaps.
- Missing from the catalog: classical, hip-hop, latin, k-pop, reggae, blues — entire listener communities are unrepresented.
- The dataset reflects one person's idea of genre diversity, not a systematic survey of global music consumption.

---

## 5. Strengths

- **Clear differentiation**: A pop/happy user and a lofi/chill user get completely different top-5 lists. The tier weighting ensures that "vibe" features dominate, which aligns with how most people describe what they want to listen to.
- **Graceful degradation with partial input**: If a user only specifies genre, the system scores only on genre. If they add energy and valence, those features join the score. The system never crashes on incomplete input.
- **Transparency**: Every recommendation comes with an explanation ("genre match; energy similarity 98%"), making it easy to understand *why* a song was picked and to spot when the logic is doing something unexpected.
- **Intuitive results for well-represented profiles**: Users whose taste matches a genre/mood combination with multiple songs in the catalog (e.g., lofi/chill has 3 songs) get nuanced rankings where energy and acousticness break ties meaningfully.

---

## 6. Limitations and Bias

- **Genre dominance bias**: Genre weight (3.0) is so high that a genre mismatch is nearly impossible to overcome. A pop song with perfect energy, mood, and valence similarity to a rock listener will still rank low. This means the system effectively filters by genre first and only uses other features as tiebreakers within the same genre.
- **Categorical rigidity**: "Indie pop" and "pop" get 0% similarity. "Rock" and "metal" are treated as unrelated. Real genre relationships are gradients, not binary.
- **Conflicting preferences are mishandled**: A user who asks for "lofi + energy 0.95" gets low-energy lofi songs because genre+mood loyalty (weight 6.0) overwhelms the energy signal (weight 2.5). The system doesn't warn the user that their preferences are contradictory.
- **Underrepresented genres get bad recommendations**: A classical music listener gets bossa nova as the "best" match (score 0.64) — the system doesn't flag that no good match exists, it just returns the least-bad option with a confident-looking score.
- **No diversity mechanism**: If 5 songs share the top genre+mood, all 5 will be recommended. There's no "also try something different" logic.
- **Small catalog ceiling**: With only 1 song per genre for most genres, the system can't differentiate between users who like the same genre but different sub-styles.

---

## 7. Evaluation

**Profiles tested**:
- High-Energy Pop, Chill Lofi, Deep Intense Rock (core profiles)
- Conflicting: lofi + energy 0.95 (adversarial)
- Missing Genre: classical (out-of-distribution)
- Numeric Only: no genre/mood (boundary test)

**What I looked for**: Whether the #1 pick matched intuition, whether edge cases produced surprising or misleading results, and whether different users actually got different recommendations.

**Findings**:
- Core profiles produced intuitive results — the right genre's best song always ranked first with scores above 0.98.
- The "Conflicting" profile revealed genre dominance: lofi songs ranked top despite terrible energy matches.
- The "Missing Genre" profile showed that mood becomes the primary signal when genre can't match — Bossa Nova Sunset won via "relaxed" mood match, which actually feels reasonable.
- The "Numeric Only" profile produced the most surprising result: a country song won because its audio features happened to be numerically close. This showed that without categorical anchors, the system becomes a pure number matcher with no "taste" awareness.

**Weight experiment**: Halving genre (3.0 → 1.5) and doubling energy (2.5 → 5.0) caused cross-genre recommendations to appear — Gym Hero (pop) jumped into the top 3 for a rock listener. The change made results feel less genre-loyal but more physically accurate.

**Automated tests**: 45 pytest cases covering scoring math, tier weight ordering, tempo normalization, edge cases (empty prefs, single-song catalog), and explanation generation.

---

## 8. Future Work

- **Genre embeddings or hierarchy**: Instead of binary match/mismatch, use a similarity matrix (e.g., rock/metal = 0.7, pop/indie pop = 0.8) so related genres partially match.
- **Conflict detection**: Warn users when their preferences are contradictory (e.g., "lofi songs rarely have energy above 0.7").
- **Diversity injection**: After picking the top match, intentionally include 1–2 songs from different genres or moods to break the filter bubble.
- **Confidence scoring**: Flag when the best match has a low absolute score, so the user knows the system is guessing rather than confident.
- **Larger dataset**: Scale to 100+ songs so each genre has enough variety to produce meaningful within-genre rankings.
- **Multi-user profiles**: Support "group vibe" recommendations where the system balances preferences across multiple listeners.

---

## 9. Personal Reflection

The most surprising thing was how much the *weights* matter compared to the *features*. Adding danceability and tempo barely changed any ranking because their low weights made them irrelevant. But shifting genre weight by 50% completely reshuffled the results. This made me realize that in real recommender systems, the tuning decisions (what to weigh, how much) are where human bias enters the system — and those decisions are usually invisible to the end user.

Building the edge case profiles changed how I think about Spotify's recommendations. When Spotify recommends a song I've never heard in a genre I don't usually listen to, that's a deliberate design choice to break the filter bubble — something my system can't do at all. And when Spotify keeps recommending the same handful of artists, that's probably the genre-dominance bias I observed here, scaled up to millions of songs. The difference between "the algorithm understands me" and "the algorithm is stuck in a loop" is just a matter of weight tuning.
