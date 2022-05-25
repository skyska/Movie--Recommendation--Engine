import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title='Movies', page_icon='🎬', layout="wide")

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=770af536001f3252cb5b24baf065feba&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    recommended_movies.append(movies.iloc[movies[movies['title'] == movie].index[0]].title)
    recommended_movies_posters.append(fetch_poster(movies.iloc[movies[movies['title'] == movie].index[0]].movie_id))

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
        print(recommended_movies_posters)
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title("Movie Recommendations")

selected_movie_name = st.selectbox('Enter the movie name', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write(names[0])
        st.image(posters[0], caption=None, width=190, use_column_width=300, clamp=False, channels="RGB", output_format="auto")

    with col2:
        st.write(names[1])
        st.image(posters[1], caption=None, width=190, use_column_width=300, clamp=False, channels="RGB", output_format="auto")
    with col3:
        st.write(names[2])
        st.image(posters[2], caption=None, width=190, use_column_width=300, clamp=False, channels="RGB", output_format="auto")
    with col4:
        st.write(names[3])
        st.image(posters[3], caption=None, width=190, use_column_width=300, clamp=False, channels="RGB", output_format="auto")
    with col5:
        st.write(names[4])
        st.image(posters[4], caption=None, width=190, use_column_width=300, clamp=False, channels="RGB", output_format="auto")
