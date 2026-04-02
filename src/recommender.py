import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic."""

    GENRE_WEIGHT = 2.0
    MOOD_WEIGHT = 1.0
    ENERGY_WEIGHT = 1.5
    VALENCE_WEIGHT = 0.5
    DANCEABILITY_WEIGHT = 0.5
    ACOUSTIC_WEIGHT = 0.8

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score a single song against a user profile and return (score, reasons)."""
        score = 0.0
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += self.GENRE_WEIGHT
            reasons.append(f"genre match: {song.genre} (+{self.GENRE_WEIGHT})")

        if song.mood.lower() == user.favorite_mood.lower():
            score += self.MOOD_WEIGHT
            reasons.append(f"mood match: {song.mood} (+{self.MOOD_WEIGHT})")

        energy_similarity = 1.0 - abs(song.energy - user.target_energy)
        energy_points = round(energy_similarity * self.ENERGY_WEIGHT, 3)
        score += energy_points
        reasons.append(f"energy similarity: {energy_similarity:.2f} (+{energy_points})")

        if user.favorite_mood.lower() == "happy":
            valence_points = round(song.valence * self.VALENCE_WEIGHT, 3)
            score += valence_points
            reasons.append(f"valence bonus: {song.valence:.2f} (+{valence_points})")

        if user.target_energy >= 0.7:
            dance_points = round(song.danceability * self.DANCEABILITY_WEIGHT, 3)
            score += dance_points
            reasons.append(f"danceability bonus: {song.danceability:.2f} (+{dance_points})")

        if user.likes_acoustic:
            acoustic_points = round(song.acousticness * self.ACOUSTIC_WEIGHT, 3)
            score += acoustic_points
            reasons.append(f"acoustic bonus: {song.acousticness:.2f} (+{acoustic_points})")

        return round(score, 3), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by score for the given user."""
        scored = [(song, self._score_song(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def recommend_with_details(
        self, user: UserProfile, k: int = 5
    ) -> List[Tuple[Song, float, List[str]]]:
        """Return top k songs with scores and explanations."""
        scored = []
        for song in self.songs:
            score, reasons = self._score_song(user, song)
            scored.append((song, score, reasons))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        score, reasons = self._score_song(user, song)
        lines = [f"Score: {score:.2f}"]
        for r in reasons:
            lines.append(f"  • {r}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Functional API (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(
    user_prefs: Dict, song: Dict, weights: Optional[Dict] = None
) -> Tuple[float, str]:
    """Score a single song dict against user preferences and return (score, explanation)."""
    if weights is None:
        weights = {
            "genre": 2.0,
            "mood": 1.0,
            "energy": 1.5,
            "valence": 0.5,
            "danceability": 0.5,
            "acousticness": 0.8,
        }

    score = 0.0
    reasons = []

    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += weights["genre"]
        reasons.append(f"genre match: {song['genre']} (+{weights['genre']})")

    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += weights["mood"]
        reasons.append(f"mood match: {song['mood']} (+{weights['mood']})")

    if "energy" in user_prefs and "energy" in song:
        energy_sim = 1.0 - abs(song["energy"] - user_prefs["energy"])
        energy_pts = round(energy_sim * weights["energy"], 3)
        score += energy_pts
        reasons.append(f"energy similarity: {energy_sim:.2f} (+{energy_pts})")

    if user_prefs.get("mood", "").lower() == "happy" and "valence" in song:
        val_pts = round(song["valence"] * weights["valence"], 3)
        score += val_pts
        reasons.append(f"valence bonus: {song['valence']:.2f} (+{val_pts})")

    if user_prefs.get("energy", 0) >= 0.7 and "danceability" in song:
        dance_pts = round(song["danceability"] * weights["danceability"], 3)
        score += dance_pts
        reasons.append(f"danceability bonus: {song['danceability']:.2f} (+{dance_pts})")

    if user_prefs.get("likes_acoustic") and "acousticness" in song:
        ac_pts = round(song["acousticness"] * weights["acousticness"], 3)
        score += ac_pts
        reasons.append(f"acoustic bonus: {song['acousticness']:.2f} (+{ac_pts})")

    explanation = "; ".join(reasons) if reasons else "no matching features"
    return round(score, 3), explanation


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Optional[Dict] = None
) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs as (song_dict, score, explanation) tuples."""
    scored = []
    for song in songs:
        s, explanation = score_song(user_prefs, song, weights)
        scored.append((song, s, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]