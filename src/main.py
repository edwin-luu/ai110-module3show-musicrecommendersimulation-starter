"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    print(f"\nUser profile: {user_prefs}")
    print("=" * 60)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nTop {len(recommendations)} recommendations:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"  {rank}. {song['title']} by {song['artist']}")
        print(f"     Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"     Score: {score:.2f}")
        print(f"     Why:   {explanation}")
        print()


if __name__ == "__main__":
    main()
