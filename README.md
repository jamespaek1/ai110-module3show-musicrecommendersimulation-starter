🎵 Music Recommender Simulation

Project Summary

This project is a content-based music recommender simulation built in Python. It represents songs as data loaded from a CSV file, defines user "taste profiles" as dictionaries of preferences, and uses a weighted scoring algorithm to rank every song in the catalog. The system awards points for genre matches, mood matches, energy similarity, and conditional bonuses for valence, danceability, and acousticness — then returns the top results with plain-language explanations of why each song was chosen.

How The System Works

Each Song in the system uses these features: genre, mood, energy (0–1 scale), tempo_bpm, valence (0–1), danceability (0–1), and acousticness (0–1).
A UserProfile stores: favorite genre, favorite mood, a target energy level (0–1), and whether the user prefers acoustic music.
The Recommender computes a score for each song using this recipe:

+2.0 points if the song's genre matches the user's favorite genre
+1.0 point if the song's mood matches the user's favorite mood
Up to +1.5 points for energy similarity, calculated as (1 - |song_energy - target_energy|) × 1.5 — songs closer to the user's preferred energy score higher
Up to +0.5 points as a valence bonus if the user prefers happy mood
Up to +0.5 points as a danceability bonus if the user's target energy is high (≥ 0.7)
Up to +0.8 points as an acoustic bonus if the user likes acoustic music

After scoring every song, the system sorts from highest to lowest and returns the top k results. Each recommendation includes a breakdown of exactly which rules contributed to its score.

Getting Started

Setup

Create a virtual environment (optional but recommended):

bash   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

Install dependencies

bash   pip install -r requirements.txt

Run the app:

bash   python -m src.main
Running Tests
Run the starter tests with:
bashpytest
You can add more tests in tests/test_recommender.py.

Experiments You Tried

Weight shift — energy ×2, genre ×0.5: Doubling the energy weight from 1.5 to 3.0 and halving genre from 2.0 to 1.0 caused genre boundaries to blur. A pop fan started seeing EDM and rock tracks that happened to share a similar energy level, 
because energy dominated the score.

Removing the mood check: Commenting out the mood match made results less nuanced. "Sad" and "happy" songs appeared side by side in the same recommendation list 
since only genre and energy differentiated them.

Edge-case profile (sad EDM + acoustic): A contradictory profile combining sad mood, EDM genre, and acoustic preference produced uniformly low scores across the board, since almost no song in the catalog matched all three conflicting signals 
at once. This exposed how the system handles unusual taste combinations.

Different user types: The High-Energy Pop profile got clean, intuitive results. The Chill Lofi profile correctly surfaced lofi and folk tracks. The Intense Rock profile returned rock and metal. Results felt right for straightforward profiles but broke down for edge cases.


Limitations and Risks

It only works on a tiny catalog of 20 songs, so recommendations can feel repetitive.

It does not understand lyrics, language, or cultural context.

Genre matching is binary — "rock" and "metal" get zero partial credit despite being closely related.

Pop is slightly overrepresented in the dataset, so pop fans get better-differentiated results than fans of underrepresented genres like jazz or country.

It has no collaborative filtering — it cannot learn from other users' behavior or listening history.

Mid-range energy songs have a subtle advantage since they are "close enough" to both high and low energy targets.


Reflection

Building this recommender taught me that even a simple weighted-score formula can produce surprisingly convincing results when the weights are balanced well. The pop and lofi profiles both received recommendations that genuinely "felt right," which shows how powerful even basic content-based filtering can be. At the same time, the edge-case profile with contradictory preferences revealed that the system has no graceful way to handle ambiguity — it just assigns low scores to everything.

The biggest lesson was about bias. The dataset's genre distribution directly controls who gets good recommendations and who gets mediocre ones. A user who likes jazz only has two songs to choose from, while a pop fan has three. In a real product at scale, this kind of imbalance could systematically disadvantage listeners with less mainstream taste — creating filter bubbles that reinforce popularity rather than helping people discover new music.

## Terminal Output

### Phase 3: Default Recommendations
![Default Pop Recommendations](default_pop_recommendations.png)

### Phase 4: Diverse Profile Testing

![Chill Lofi Recommendations](chill_lofi_recommendations.png)

![Intense Rock Recommendations](intense_rock_recommendations.png)

![Edge Case Recommendations](edge_case_recommendations.png)

### Experiment: Weight Shift
![Experiment Weight Shift](experiment_weight_shift.png)