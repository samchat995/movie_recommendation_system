import streamlit as st
import pandas as pd
import pickle

from src.recommender import MovieRecommender


movies = pd.read_csv( "data/processed/imdb_preprocessed.csv")

with open("models/tfidf_matrix.pkl", "rb") as file:
    tfidf_matrix = pickle.load(file)


recommender = MovieRecommender(
    movies,
    tfidf_matrix
)    

st.title("🎬 Mood-Based Movie Recommendation System")

st.write(
    "Tell me how you're feeling and I'll recommend movies for you."
)

user_input = st.text_input(
    "How are you feeling today?"
)

favourite_movie = st.text_input(
    "What's your favourite movie?"
)

recommend_button = st.button(
    "🎬 Recommend Movies"
)


if recommend_button:

    if not user_input:
        st.warning("Please tell me how you're feeling.")

    elif not favourite_movie:
        st.warning("Please enter your favourite movie.")

    else:
      result = recommender.recommend(
             mood_input=user_input,
             favourite_movie=favourite_movie,
             top_n=10
            )

       

        # Detected Mood
      st.subheader("🧠 Detected Mood")

      st.success(
            result["predicted_mood"].capitalize()
        )

        # Matched Movie
      st.subheader("🎬 Your Movie")

      st.write(
            result["matched_movie"]
        )

        # Recommendations
      st.subheader("🍿 Recommended Movies")

      recommendations = result["recommendations"]

      recommendations = result["recommendations"]

      display_recommendations = recommendations[
          ["movie_name", "year", "similarity_score"]
      ].reset_index(drop=True)

      st.dataframe(
          display_recommendations,
          use_container_width=True,
          hide_index=True
      )
        

        # Movie Details
      for _, movie in recommendations.iterrows():

            st.write(
                f"### 🎬 {movie['movie_name']}"
            )

            st.write(
                f"Year: {movie['year']}"
            )

            st.write(
                f"Similarity: {movie['similarity_score']:.2f}"
            )

            st.divider()
              