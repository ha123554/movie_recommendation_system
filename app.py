import streamlit as st
import pickle
import requests
import gdown

# Google Drive file IDs
movies_file_id = "1hN780rSbePArfHLiFTh6oZOQOF5dF96R"
similarity_file_id = "1xjoOee3VFQlArvvAzUOuvtrpb9GzPRwU"

# Download files (will save locally)
gdown.download(f"https://drive.google.com/uc?id={movies_file_id}", "movies.pkl", quiet=False)
gdown.download(f"https://drive.google.com/uc?id={similarity_file_id}", "similarity.pkl", quiet=False)

# Load pickle files
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))



# -----------------------------
# TMDB API poster fetch function
# -----------------------------
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=ed2067864e3dde5a91dc6753833ee565&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# -----------------------------
# Recommendation function
# -----------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # get actual TMDB movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Movie Recommender System")

# Dropdown for movie selection
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

# Show recommendations when button clicked
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display recommended movies and posters
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.text(names[idx])
        col.image(posters[idx])
