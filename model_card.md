# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

VibeFinder 1.0

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration 

This recommender suggests 3–5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration of how content-based recommendation systems work. It is not intended for production use with real listeners.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

The system looks at each song in the catalog and asks a series of questions: Does this song's genre match what the user likes? Does the mood match? Is the energy level close to their target? Depending on the answers, it awards points. Genre matches are worth the most (2 points), mood matches add 1 point, and energy similarity contributes up to 1.5 points based on how close the values are. There are smaller bonuses for valence, danceability, and acousticness depending on the user's profile. After scoring every song, it sorts them from highest to lowest and returns the top results along with a plain-language explanation of why each song earned its score.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog contains 20 songs stored in data/songs.csv. Genres represented include pop, rock, edm, lofi, folk, metal, hip-hop, r&b, jazz, synthwave, indie, and country. Moods include happy, chill, sad, and intense. The original starter dataset had 10 songs and was expanded with 10 additional tracks to improve diversity. Pop is still slightly overrepresented (3 out of 20 songs). The dataset does not include any Latin, K-pop, classical, or African music genres, so users who prefer those styles will receive poor recommendations.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works well for users whose taste aligns neatly with a single genre and mood — for example, a "happy pop" listener or a "chill lofi" listener gets results that feel intuitively correct. The explanation feature makes the scoring transparent so users (and developers) can see exactly why a song was chosen. The modular design makes it easy to adjust weights and immediately see how the output changes.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The system does not consider lyrics, artist popularity, release date, or any social signals like what friends are listening to. Genre matching is all-or-nothing — "rock" and "metal" are treated as completely unrelated. The small catalog means the system has very few options to choose from, so recommendations can feel repetitive. Because pop has the most entries, users with pop preferences tend to get better-differentiated results than users who prefer underrepresented genres like jazz or country. The energy-based scoring also slightly favors mid-range energy songs since they are "close enough" to both high and low energy targets, which could create a subtle bias toward moderate-energy tracks.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

Four user profiles were tested: High-Energy Pop Fan, Chill Lofi Listener, Intense Rock Lover, and an edge case combining sad mood with EDM genre and acoustic preference. For the first three profiles, the top results matched expectations — the pop fan saw pop songs, the lofi listener got lofi and folk tracks, and the rock lover received rock and metal. The edge-case profile produced uniformly low scores, which correctly reflected that no song in the catalog matches such a contradictory set of preferences. One experiment doubled the energy weight and halved the genre weight, which caused genre boundaries to blur and energy-similar songs from different genres to rise in rank. This confirmed that the weighting system is sensitive and that genre dominance can be tuned down if desired.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

If this project continued, I would add partial genre matching (so "rock" and "metal" share some credit), introduce a diversity penalty to prevent too many songs from the same artist appearing in the top results, expand the catalog to at least 100 songs across more genres, and add a simple web UI using Streamlit so users can adjust their preferences with sliders and see results update in real time. Supporting multiple users and comparing their profiles for "group playlist" generation would also be an interesting extension.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

The most surprising thing was how much the dataset composition matters. Even with a well-designed scoring algorithm, the recommendations are only as diverse as the catalog itself. Building this also made me realize that the "magic" of Spotify's Discover Weekly is less about a single clever formula and more about the massive scale of data and continuous feedback loops. Using AI tools helped me brainstorm scoring strategies and debug edge cases quickly, but I still had to make judgment calls about what weights "felt right" — which reminded me that human intuition still plays a central role even in algorithmic systems.