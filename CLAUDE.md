# Music Recommender Simulation

## Project Overview
A content-based music recommender system for CodePath AI110 Module 3. Scores songs against a user taste profile using tier-weighted feature similarity.

## Architecture

### Two execution paths (both must work):
- **Functional**: `src/main.py` -> `load_songs()`, `recommend_songs()`, `score_song()` (dict-based)
- **OOP**: `tests/` -> `Recommender` class with `Song` / `UserProfile` dataclasses

The OOP path delegates scoring to the functional `score_song()` to avoid duplication.

### Key files:
- `src/recommender.py` — All recommendation logic: data classes, scoring, loading, explanation
- `src/main.py` — CLI runner, imports from `recommender` (no `src.` prefix)
- `tests/test_recommender.py` — Pytest suite, imports from `src.recommender`
- `data/songs.csv` — 18 songs, 7 features (genre, mood, energy, tempo_bpm, valence, danceability, acousticness)

### Import convention:
- `main.py` uses `from recommender import ...` (run via `python -m src.main`)
- Tests use `from src.recommender import ...`

## Scoring Design

### Formula:
```
score = sum(weight[f] * similarity[f]) / sum(weight[f])  for active features
```
Normalized to [0, 1]. Only features present in user prefs are scored.

### Feature tiers & default weights:
| Tier | Features | Weights |
|------|----------|---------|
| 1 (vibe) | genre (3.0), mood (3.0), energy (2.5) | Highest |
| 2 (support) | acousticness (1.5), valence (1.5) | Medium |
| 3 (tiebreaker) | danceability (0.75), tempo_bpm (0.5) | Lowest |

### Similarity functions:
- Categorical (genre, mood): 1.0 exact match, 0.0 otherwise
- Numeric 0-1 (energy, valence, danceability, acousticness): `1 - abs(user - song)`
- tempo_bpm: normalize via `(bpm - 60) / (200 - 60)` clamped to [0,1], then same formula
- likes_acoustic (bool): converted to numeric target (True -> 0.8, False -> 0.2)

## Commands
```bash
python -m src.main          # Run recommender
pytest                       # Run tests
pytest -v                    # Run tests verbose
pytest tests/test_recommender.py::TestScoreSong  # Run specific test class
```

## Data
- 18 songs in `data/songs.csv`
- Genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, electronic, r&b, metal, bossa nova, chiptune, folk, house
- Moods: happy, chill, intense, relaxed, focused, moody, nostalgic, energetic, romantic, aggressive, playful, melancholy
- All numeric features 0-1 except tempo_bpm (60-168)
