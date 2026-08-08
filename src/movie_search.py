from rapidfuzz import process


class MovieSearch:

    def __init__(self, dataframe):
        self.movies = dataframe

        # Store all movie names
        self.movie_names = dataframe["movie_name"].tolist()

    def find_movie(self, user_input, score_cutoff=70):

        result = process.extractOne(
            user_input,
            self.movie_names,
            score_cutoff=score_cutoff
        )

        if result is None:
            return None

        matched_movie, score, _ = result
        print(f"Matched movie: {matched_movie} ({score:.1f}%)")

        return matched_movie

    def find_movie_index(self, user_input):
         matched_movie = self.find_movie(user_input)

         if matched_movie is None:
            return None

         match = self.movies[
            self.movies["movie_name"] == matched_movie
        ]

         if match.empty:
            return None

         return match.index[0]
