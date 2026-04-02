
from src.recommender import Song, UserProfile, Recommender


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1, title="Test Pop Track", artist="Test Artist",
            genre="pop", mood="happy", energy=0.8, tempo_bpm=120,
            valence=0.9, danceability=0.8, acousticness=0.2,
        ),
        Song(
            id=2, title="Chill Lofi Loop", artist="Test Artist",
            genre="lofi", mood="chill", energy=0.4, tempo_bpm=80,
            valence=0.6, danceability=0.5, acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop", favorite_mood="happy",
        target_energy=0.8, likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop", favorite_mood="happy",
        target_energy=0.8, likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_score_increases_with_genre_match():
    user = UserProfile(
        favorite_genre="pop", favorite_mood="chill",
        target_energy=0.5, likes_acoustic=False,
    )
    rec = make_small_recommender()
    pop_song = rec.songs[0]   # genre=pop
    lofi_song = rec.songs[1]  # genre=lofi

    pop_score = rec._score_song(user, pop_song)[0]
    lofi_score = rec._score_song(user, lofi_song)[0]
    assert pop_score > lofi_score


def test_acoustic_bonus_applied():
    user = UserProfile(
        favorite_genre="lofi", favorite_mood="chill",
        target_energy=0.4, likes_acoustic=True,
    )
    rec = make_small_recommender()
    lofi_song = rec.songs[1]  # acousticness=0.9

    _, reasons = rec._score_song(user, lofi_song)
    reason_text = " ".join(reasons)
    assert "acoustic bonus" in reason_text