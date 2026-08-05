import numpy as np


class MovieRecommender:

    def __init__(self, dataframe, tfidf_matrix):

        self.movies = dataframe
        self.tfidf_matrix = tfidf_matrix