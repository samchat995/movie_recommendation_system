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

st.title("🎬 MoodFlix")
st.subheader("Movie recommendations based on how you feel")

st.write(
    "Tell me your mood and a movie you love. "
    "I'll find movies that match your mood and taste."
)

col1, col2 = st.columns(2)

with col1:
    user_input = st.text_input(
        "How are you feeling today?"
    )

with col2:
    st.caption(
    "Examples: "
    "I'm feeling stressed and want something relaxing, "
    "I'm excited and want something intense."
)
    favourite_movie = st.text_input(
        "What's your favourite movie?"
    )

recommend_button = st.button(
    "🎬 Recommend Movies"
)


if recommend_button:

    if not user_input.strip():
        st.warning("Please describe how you're feeling.")

    elif not favourite_movie.strip():
        st.warning("Please enter your favourite movie.")

    else:
      top_n = st.slider(
        "Number of recommendations",
         min_value=5,
         max_value=10,
         value=10
      )
      with st.spinner("🎬 Finding movies for you..."):    
        result = recommender.recommend(
             mood_input=user_input,
             favourite_movie=favourite_movie,
             top_n=top_n
            )

       

        # Detected Mood
      st.subheader("🧠 Detected Mood")

      detected_mood = result["predicted_mood"]

      st.subheader("🧠 Your Mood")

      st.success(
          f"You seem to be feeling **{detected_mood.capitalize()}**"
      )

        # Matched Movie
      st.subheader("❤️ Based on your favourite")

      st.info(
          f"Matched movie: **{result['matched_movie']}**"
      )

        # Recommendations
      st.subheader("🍿 Recommended Movies")

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
      st.subheader("🍿 Recommended Movies")

      for i, (_, movie) in enumerate(recommendations.iterrows(),start=1):
          st.write(
            f"### {i}. 🎬 {movie['movie_name']}"
          )

          st.write(
            f"Year: {movie['year']}  |  "
            f"Similarity: {movie['similarity_score']:.2%}"
          )

          st.divider()
              