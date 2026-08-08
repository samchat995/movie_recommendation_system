from sklearn.metrics.pairwise import cosine_similarity

from src.movie_search import MovieSearch
from src.movie_filter import MovieFilter
from src.mood_classifier import MoodClassifier
from src.genre_mapper import MOOD_GENRES


class MovieRecommender:

    def __init__(self, dataframe, tfidf_matrix):

        self.movies = dataframe
        self.tfidf_matrix = tfidf_matrix
        self.movie_search = MovieSearch(dataframe)
        self.classifier = MoodClassifier()
        self.filter = MovieFilter(dataframe)

    def recommend(
        self,
        mood_input,
        favourite_movie,
        top_n=10
    ):
        # Step 1: Predict Mood
        prediction = self.classifier.predict(mood_input)

        if isinstance(prediction, dict):
            mood = prediction["mood"]
            confidence = prediction["confidence"]
        else:
            mood = prediction
            confidence = None

        print(f"Predicted Mood : {mood}")

        if confidence is not None:
            print(f"Mood Confidence : {confidence:.0%}")

        # Step 2: Get Genres
        genres = MOOD_GENRES.get(mood)

        if genres is None:
            raise ValueError(
                f"No genre mapping found for mood '{mood}'."
    )

        print(f"Selected Genres : {genres}")

        # Step 3: Candidate Generation
        candidate_movies = self.filter.filter_by_genres(genres)

        candidate_indices = candidate_movies.index.tolist()

        if len(candidate_indices) == 0:
            raise ValueError(
                f"No movies found matching genres {genres} for mood '{mood}'."
            )

        # Find the closest matching movie name and its index
        favourite_index = self.movie_search.find_movie_index(favourite_movie)

        if favourite_index is None:
            raise ValueError(
                f"No movie found similar to '{favourite_movie}'."
            )

        # Get the matched movie name for the return value
        matched_movie = self.movies.loc[favourite_index, "movie_name"]

        print(f"Matched Movie: {matched_movie}")

        # Check if the favourite movie is in the candidate set
        if favourite_index not in candidate_indices:
            # Add the favourite movie to the candidate set
            candidate_indices = candidate_indices + [favourite_index]

        # TF-IDF vector of favourite movie
        favourite_vector = self.tfidf_matrix[favourite_index]

        # TF-IDF vectors of candidate movies
        candidate_vectors = self.tfidf_matrix[candidate_indices]

        # Calculate cosine similarity
        similarity_scores = cosine_similarity(
            favourite_vector,
            candidate_vectors
        ).flatten()

        # Create recommendations dataframe
        recommendations = self.movies.loc[candidate_indices].copy()

        recommendations["similarity_score"] = similarity_scores

        # Remove the favourite movie itself
        recommendations = recommendations[
            recommendations.index != favourite_index
        ]

        # Sort by similarity
        recommendations = recommendations.sort_values(
            by="similarity_score",
            ascending=False
        )

        # Return Top N recommendations
        return {
            "predicted_mood": mood,
            "matched_movie": matched_movie,
            "recommendations": recommendations.head(top_n)
        }
