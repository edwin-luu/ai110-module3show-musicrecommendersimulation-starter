# 🎵 Music Recommender Simulation

## Personal Notes
Collaborative Filtering: if Song X and Song Y frequently appear in the same playlists, they're considered related.
  - "Users like you also liked..."
  - Strength: surprise factor, discovery of unrelated songs for a person.
  - Weakness: new listeners get zero recommendations; popular tracks may get favored.

Content-Based Filtering: songs with similar characteristics are recommended.
  - Strength: no listening history is required; just listen to one song and you get recommended something similar.
  - Weakness: only recommended more of the "same" songs.



Dataset Overview
  - Your songs.csv has 10 songs with 7 features split into two types:

  ┌──────────────┬───────────────┬─────────────────────────────────────────────────────────────────┬─────────────────┐
  │   Feature    │     Type      │                          Range in Data                          │ Example Spread  │
  ├──────────────┼───────────────┼─────────────────────────────────────────────────────────────────┼─────────────────┤
  │ genre        │ Categorical   │ 6 values (pop, lofi, rock, ambient, jazz, synthwave, indie pop) │ Discrete labels │
  ├──────────────┼───────────────┼─────────────────────────────────────────────────────────────────┼─────────────────┤
  │ mood         │ Categorical   │ 5 values (happy, chill, intense, relaxed, focused, moody)       │ Discrete labels │
  ├──────────────┼───────────────┼─────────────────────────────────────────────────────────────────┼─────────────────┤
  │ energy       │ Numeric (0-1) │ 0.28 – 0.93                                                     │ Wide spread     │
  ├──────────────┼───────────────┼─────────────────────────────────────────────────────────────────┼─────────────────┤
  │ tempo_bpm    │ Numeric       │ 60 – 152                                                        │ Wide spread     │
  ├──────────────┼───────────────┼─────────────────────────────────────────────────────────────────┼─────────────────┤
  │ valence      │ Numeric (0-1) │ 0.48 – 0.84                                                     │ Moderate spread │
  ├──────────────┼───────────────┼─────────────────────────────────────────────────────────────────┼─────────────────┤
  │ danceability │ Numeric (0-1) │ 0.41 – 0.88                                                     │ Moderate spread │
  ├──────────────┼───────────────┼─────────────────────────────────────────────────────────────────┼─────────────────┤
  │ acousticness │ Numeric (0-1) │ 0.05 – 0.92                                                     │ Wide spread     │
  └──────────────┴───────────────┴─────────────────────────────────────────────────────────────────┴─────────────────┘

  
Feature-by-Feature Assessment
  Tier 1: Strongest "Vibe" Indicators

  genre + mood — These are the most intuitive, human-readable filters. When someone says "I want chill lofi," they're already using these two features. They act as coarse-grained filters that immediately narrow 
  the field. In the dataset, the combination of genre+mood cleanly separates distinct listening contexts (study session vs. workout vs. driving).

  energy — This is arguably the single most powerful numeric feature. It cleanly separates "Spacewalk Thoughts" (0.28, ambient chill) from "Gym Hero" (0.93, intense pop). Energy maps directly to how music feels 
  physically — are you nodding off or bouncing? It also has the widest practical spread in the dataset.

  Tier 2: Strong Supporting Features

  acousticness — Has the widest numeric spread (0.05 to 0.92) and captures a real vibe divide: electronic/produced sounds vs. organic/intimate sounds. "Gym Hero" at 0.05 feels completely different from
  "Spacewalk Thoughts" at 0.92, even beyond energy. The UserProfile already has likes_acoustic as a boolean, which shows the project designers considered this important.

  valence — Measures musical positivity/happiness. "Sunrise City" (0.84) sounds uplifting; "Storm Runner" (0.48) sounds darker. This adds emotional nuance that mood alone can't capture — two "chill" songs can   
  have different emotional tones.

  Tier 3: Useful but Secondary

  danceability — Matters in specific contexts (party playlists) but overlaps heavily with energy. In this dataset, high-energy songs tend to be high-danceability too. It adds less unique information.

  tempo_bpm — Objectively measurable but less perceptually meaningful on its own. A 120 BPM pop song and a 120 BPM jazz song feel nothing alike. Tempo is also on a different scale (60-152) vs. the 0-1 features, 
  so it needs normalization. Useful as a tiebreaker, not a primary signal.


## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world music recommenders like Spotify use two main approaches: collaborative filtering ("users like you also liked...") and content-based filtering (matching song characteristics to your taste). This system uses **content-based filtering** — it compares each song's audio features against a user's taste profile and produces a similarity score. The key design choice is a **tier-weighted scoring system**, where not all features are treated equally. Genre, mood, and energy are weighted heaviest because they define the core "vibe" of a song, while features like danceability and tempo serve as tiebreakers. The final score is normalized to [0, 1], and the top-k songs are returned as recommendations.

### Song Features

Each `Song` carries 7 measurable features:

| Feature | Type | Role |
|---|---|---|
| `genre` | Categorical | Tier 1 — primary vibe filter |
| `mood` | Categorical | Tier 1 — emotional context |
| `energy` | Numeric (0-1) | Tier 1 — physical intensity |
| `acousticness` | Numeric (0-1) | Tier 2 — organic vs. produced sound |
| `valence` | Numeric (0-1) | Tier 2 — musical positivity |
| `danceability` | Numeric (0-1) | Tier 3 — rhythmic suitability |
| `tempo_bpm` | Numeric (60-200) | Tier 3 — speed (normalized to 0-1 for scoring) |

### UserProfile Fields

| Field | Type | Purpose |
|---|---|---|
| `favorite_genre` | str | Preferred genre to match against |
| `favorite_mood` | str | Preferred mood to match against |
| `target_energy` | float | Desired energy level (0-1) |
| `likes_acoustic` | bool | Acoustic preference (converted to 0.8/0.2 for scoring) |
| `target_valence` | float (optional) | Desired positivity level |
| `target_danceability` | float (optional) | Desired danceability level |
| `target_tempo_bpm` | float (optional) | Desired tempo |

### Scoring

The recommender scores each song by computing weighted similarity across only the features the user has specified:

```
score = sum(weight[f] * similarity(user[f], song[f])) / sum(weight[f])
```

Songs are ranked by score descending, and the top k are returned with human-readable explanations of why each song was recommended.

### CLI Output

![Recommendations output](recommendations_ss.jpg)

### Data Flow

```mermaid
flowchart TD
    A[User Profile] --> C[Scoring Loop]
    B[songs.csv] --> C
    C -->|For each song| D{Compute Weighted Similarity}
    D -->|Categorical: genre, mood| E[1.0 if match, 0.0 if not]
    D -->|Numeric: energy, valence, etc.| F["1.0 - abs(user - song)"]
    E --> G[Multiply by tier weight]
    F --> G
    G --> H[Sum & normalize to 0-1 score]
    H --> I[Sort all songs by score descending]
    I --> J[Return top k with explanations]
```

### Expected Biases and Limitations

- **Genre dominance**: Genre has the highest weight (3.0), so a genre mismatch is hard to overcome even if every other feature is a perfect match. This means the system may never recommend a great song outside the user's stated genre.
- **Categorical rigidity**: Genre and mood use exact-match scoring — "indie pop" gets 0 similarity with "pop" even though they are closely related. Real systems use genre embeddings or hierarchies to capture partial similarity.
- **Small catalog bias**: With only 18 songs, some genres have just one representative. A user who likes "folk" will always get the same recommendation regardless of other preferences.
- **No discovery**: Content-based filtering inherently recommends "more of the same." It cannot surface a surprising song the way collaborative filtering can.
- **Energy-tempo overlap**: High-energy songs tend to have high tempo and danceability, so Tier 3 features rarely change the ranking in practice — they mostly confirm what Tier 1 already decided.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Experiment 1: Weight Shift — Double Energy, Halve Genre

Changed `genre` weight from 3.0 to 1.5 and `energy` weight from 2.5 to 5.0.

**Results**: For the "Deep Intense Rock" profile, "Gym Hero" (pop, intense, energy=0.93) jumped from #3 to #2, overtaking "Iron Anthem" (metal, aggressive, energy=0.97). With energy dominating the score, the system cared less that Gym Hero is pop — its near-perfect energy match carried it. This made results feel *less* genre-aware but *more* physically accurate. For chill profiles the change was minimal because lofi songs already had close energy values.

**Takeaway**: Genre weight acts as a coarse filter. When you lower it, the system starts cross-pollinating genres, which can feel like discovery or feel like noise depending on the listener.

### Experiment 2: Diverse Profile Testing

![High-Energy Pop](s4_1.jpg)
![Chill Lofi](s4_2.jpg)
![Deep Intense Rock](s4_3.jpg)
![Conflicting: High-Energy Chill](s4_4.jpg)
![Missing Genre: Classical](s4_5.jpg)
![Numeric Only](s4_6.jpg)

| Profile | Top Pick | Surprising? |
|---|---|---|
| High-Energy Pop | Sunrise City (0.99) | No — perfect match |
| Chill Lofi | Library Rain (0.99) | No — perfect match |
| Deep Intense Rock | Storm Runner (0.99) | No — perfect match |
| Conflicting: lofi + energy 0.95 | Midnight Coding (0.84) | Yes — genre/mood loyalty beat energy completely |
| Missing Genre: classical | Bossa Nova Sunset (0.64) | Yes — decent fallback via mood match |
| Numeric Only (no genre/mood) | Desert Highway (0.94) | Yes — country song wins on pure audio similarity |

**Key observation**: The "Conflicting" profile revealed that genre+mood (combined weight 6.0) so heavily outweigh energy (2.5) that the system will recommend a low-energy lofi song to someone who asked for energy=0.95. This is the genre dominance bias in action.

**Profile comparisons**:
- *High-Energy Pop vs Chill Lofi*: Completely different top 5 — shows the system differentiates well when genre+mood+energy all point in different directions.
- *Deep Intense Rock vs High-Energy Pop*: Both have high energy, but genre separates them cleanly. Gym Hero (pop, intense) appears in both lists but at different ranks.
- *Conflicting vs Chill Lofi*: Nearly identical top 3 despite wildly different energy targets — confirms genre dominance drowns out numeric features when they conflict.
- *Numeric Only*: Without genre/mood, the system becomes a pure audio-feature matcher. Desert Highway (country) wins because its numeric profile happens to be close — a genre the user never asked for. This shows content-based filtering can accidentally recommend outside a listener's taste when categorical anchors are missing.

---

## Limitations and Risks

- **Tiny catalog**: 18 songs means many genres have only 1 representative, making recommendations repetitive.
- **No lyric or language understanding**: A Spanish bossa nova and an English jazz song are compared purely on audio features.
- **Genre dominance**: The system over-prioritizes genre matching. A pop song with perfect energy/mood/valence similarity to a rock listener will still rank low because genre carries weight 3.0.
- **No partial genre matching**: "indie pop" and "pop" score 0 similarity despite being closely related. "Rock" and "metal" are treated as completely unrelated.
- **Filter bubble**: The system only recommends "more of the same" — it cannot surprise a user with something outside their stated preferences.

See [model_card.md](model_card.md) for deeper analysis.

---

## Reflection

[**Model Card**](model_card.md)

Building this recommender taught me that the "algorithm" behind music recommendations is fundamentally a set of human choices disguised as math. Every weight I assigned — genre at 3.0, danceability at 0.75 — is a subjective opinion about what matters most when people pick music. The system doesn't "know" that rock and metal are related, or that a chill mood and a relaxed mood feel similar. It only knows what I told it, and the gaps in my definitions become the system's blind spots.

The bias risks became concrete when I tested edge cases. A user who likes "classical" gets zero genre matches because classical doesn't exist in the catalog — the system doesn't fail gracefully, it just quietly gives bad recommendations with moderate confidence scores. In a real product, this would disproportionately affect listeners of underrepresented genres. The "Conflicting" profile (lofi + high energy) showed how rigid categorical matching overrides numeric signals, meaning the system would rather recommend a wrong-energy song in the right genre than a right-energy song in the wrong genre. Whether that's a feature or a bug depends on the listener — and that ambiguity is exactly where real-world recommender bias lives.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

