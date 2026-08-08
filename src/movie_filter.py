import re


class MovieFilter:

    def __init__(self, dataframe):
        self.movies = dataframe

    def filter_by_genres(self, genres):

        if "tags" not in self.movies.columns:
            raise ValueError

        # Escape each genre to avoid regex special character issues
        escaped_genres = [re.escape(genre) for genre in genres]

        pattern = "|".join(escaped_genres)

        filtered = self.movies[
            self.movies["tags"].str.contains(
                pattern,
                case=False,
                na=False
            )
        ]

        return filtered

    def get_candidate_indices(self, genres):
        """Return the list of indices for movies matching the given genres."""

        filtered = self.filter_by_genres(genres)

        return filtered.index.tolist()
