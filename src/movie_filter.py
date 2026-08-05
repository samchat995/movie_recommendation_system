import pandas as pd

class MovieFilter:

    def __init__(self, dataframe):
        self.movies = dataframe

    def filter_by_genres(self, genres):

        pattern = "|".join(genres)

        filtered = self.movies[
            self.movies["tags"].str.contains(
                pattern,
                case=False,
                na=False
            )
        ]

        return filtered


   