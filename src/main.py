"""
Command line runner for the Music Recommender Simulation.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4, "acousticness": 0.85},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "valence": 0.45},
    # Edge case: conflicting preferences (high energy but chill mood)
    "Conflicting: High-Energy Chill": {"genre": "lofi", "mood": "chill", "energy": 0.95},
    # Edge case: genre not in catalog
    "Missing Genre: Classical": {"genre": "classical", "mood": "relaxed", "energy": 0.3},
    # Edge case: only numeric prefs, no genre/mood
    "Numeric Only": {"energy": 0.5, "valence": 0.7, "danceability": 0.6, "acousticness": 0.8},
}


def print_recommendations(name, prefs, songs, k=5):
    print(f"\n{'=' * 60}")
    print(f"  Profile: {name}")
    print(f"  Prefs:   {prefs}")
    print(f"{'=' * 60}")

    results = recommend_songs(prefs, songs, k=k)

    for rank, (song, score, explanation) in enumerate(results, 1):
        print(f"  {rank}. {song['title']} by {song['artist']}")
        print(f"     Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"     Score: {score:.2f}")
        print(f"     Why:   {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
