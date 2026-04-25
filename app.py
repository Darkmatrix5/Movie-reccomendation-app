import pickle
from pathlib import Path
import streamlit as st
import requests

FALLBACK_POSTER = "https://via.placeholder.com/500x750?text=No+Poster"

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        data = requests.get(url, timeout=10).json()
        poster_path = data.get("poster_path")
        if not poster_path:
            return FALLBACK_POSTER
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    except requests.RequestException:
        return FALLBACK_POSTER

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    recommended_movie_names = []
    recommended_movie_posters = []
    for neighbor_idx, _score in distances[:5]:
        # fetch the movie poster
        movie_id = movies.iloc[neighbor_idx].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[neighbor_idx].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')

def load_pickle(filename):
    base_dir = Path(__file__).resolve().parent
    candidates = [base_dir / "model" / filename, base_dir / filename]
    for path in candidates:
        if path.exists():
            with open(path, "rb") as f:
                return pickle.load(f)
    raise FileNotFoundError(
        f"{filename} not found. Checked: {candidates[0]} and {candidates[1]}"
    )


movies = load_pickle("movie_list.pkl")
similarity = load_pickle("similarity.pkl")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])





