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