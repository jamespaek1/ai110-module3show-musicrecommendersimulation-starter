"""
Command-line runner for the Music Recommender Simulation.
Run with:  python3 -m src.main
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(profile_name, user_prefs, songs, k=5):
    """Print formatted recommendations for a given user profile."""
    print("=" * 60)
    print(f"  Profile: {profile_name}")
    print(f"  Prefs:   {user_prefs}")
    print("=" * 60)

    results = recommend_songs(user_prefs, songs, k=k)

    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"\n  #{rank}  {song['title']}  by {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"       Score: {score:.2f}")
        print(f"       Because: {explanation}")

    print("\n")


def main():
    songs = load_songs("data/songs.csv")

    # --- Profile 1: High-Energy Pop ---
    pop_profile = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }
    print_recommendations("High-Energy Pop Fan", pop_profile, songs)

    # --- Profile 2: Chill Lofi Listener ---
    lofi_profile = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.3,
        "likes_acoustic": True,
    }
    print_recommendations("Chill Lofi Listener", lofi_profile, songs)

    # --- Profile 3: Intense Rock Lover ---
    rock_profile = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    }
    print_recommendations("Intense Rock Lover", rock_profile, songs)

    # --- Profile 4 (Edge Case): Conflicting Preferences ---
    edge_profile = {
        "genre": "edm",
        "mood": "sad",
        "energy": 0.9,
        "likes_acoustic": True,
    }
    print_recommendations("Edge Case: Sad EDM + Acoustic", edge_profile, songs)

    # --- Experiment: Double energy weight, halve genre weight ---
    print("*" * 60)
    print("  EXPERIMENT: energy x2, genre x0.5")
    print("*" * 60)
    exp_weights = {
        "genre": 1.0,
        "mood": 1.0,
        "energy": 3.0,
        "valence": 0.5,
        "danceability": 0.5,
        "acousticness": 0.8,
    }
    results = recommend_songs(pop_profile, songs, k=5, weights=exp_weights)
    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"\n  #{rank}  {song['title']}  by {song['artist']}  — Score: {score:.2f}")
        print(f"       Because: {explanation}")
    print("\n")


if __name__ == "__main__":
    main()