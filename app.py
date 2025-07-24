import pickle

import streamlit as st
import pandas as pd
import numpy as np
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e2fa686d278505ceeadbe43ec1fec53e"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movie_list = []
    recommend_movie_posters=[]

    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommend_movie_list.append(movies.iloc[i[0]].title)
        recommend_movie_posters.append(fetch_poster(movie_id))
    return recommend_movie_list, recommend_movie_posters



movies_dict=pickle.load(open('movie_dict', 'rb'))
movies=pd.DataFrame(movies_dict)

from io import BytesIO

from io import BytesIO

def load_similarity_from_gdrive():
    import requests
    import pickle

    # Direct download link from Google Drive
    url = "https://drive.google.com/uc?export=download&id=1lFmXEiXUE4f6L2rtHicGHvwiu1AyoU_j"
    
    response = requests.get(url)
    response.raise_for_status()

    # Convert response to BytesIO and load with pickle
    file_data = BytesIO(response.content)

    try:
        return pickle.load(file_data)
    except Exception as e:
        print("❌ Error loading pickle file:", e)
        return None
        
similarity = load_similarity_from_gdrive()

st.title("Movie Recommendation System")
selected_movie_name = st.selectbox('Enter the movie name',movies['title'].values)

if st.button('Recommend'):
    names,posters =recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.write(names[0])
        st.image(posters[0])
    with col2:
        st.write(names[1])
        st.image(posters[1])
    with col3:
        st.write(names[2])
        st.image(posters[2])
    with col4:
        st.write(names[3])
        st.image(posters[3])
    with col5:
        st.write(names[4])
        st.image(posters[4])

