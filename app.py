from ast import List
import pickle
import streamlit as st
import requests as r


movie_list = pickle.load(open('model/movie_list.pickle', 'rb'))
similarity = pickle.load(open('model/similarity.pickle', 'rb'))
api_key= ''

def get_poster(movie_id):
    api_request = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(
        movie_id, api_key)
    data = r.get(api_request)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommed_movies(movie: str) -> list:
    index = movie_list[movie_list['original_title'] == movie].index[0]

    l = []
    poster = []

    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:11]
    for i in distances:
        l.append(movie_list.iloc[i[0]].original_title)
        poster.append(get_poster(movie_list.iloc[i[0]].movie_id))
    return l, poster

# recommed_movies('Batman Forever')


st.header('Content-based recommendation system ')

option = st.selectbox(
    'Select Movie for here',
    movie_list['original_title'])

recommended_list, poster = recommed_movies(option)
 

col = st.columns(5)
# Iterate over the images and display them in columns
for i, movie_name in enumerate(recommended_list):
    pos = i % 5
    with col[pos]:
        st.text(movie_name)
        st.image(poster[i])
