import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:

    def __init__(self, dataframe, tfidf_matrix):

        self.movies = dataframe
        self.tfidf_matrix = tfidf_matrix

    def recommend(
        self,
        favourite_movie,
        candidate_indices,
        top_n=10
    ):

        # Find favourite movie
        movie = self.movies[
            self.movies["movie_name"].str.lower()
            ==
            favourite_movie.lower()
        ]

        if movie.empty:
            raise ValueError(
                f"{favourite_movie} not found in dataset."
            )

        favourite_index = movie.index[0]

        # TF-IDF vector of favourite movie
        favourite_vector = self.tfidf_matrix[favourite_index]

        # Candidate vectors
        candidate_vectors = self.tfidf_matrix[candidate_indices]

        # Similarity
        similarity_scores = cosine_similarity(
            favourite_vector,
            candidate_vectors
        ).flatten()

        recommendations = self.movies.loc[
            candidate_indices
        ].copy()

        recommendations["similarity_score"] = similarity_scores

        # Remove favourite movie if it appears
        recommendations = recommendations[
            recommendations.index != favourite_index
        ]

        recommendations = recommendations.sort_values(
            by="similarity_score",
            ascending=False
        )

        return recommendations.head(top_n)