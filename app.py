import numpy as np
import pandas as pd
import pickle
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

new_df = pd.read_csv('mov_df.csv')
cs_cv_f = pickle.load(open('cv_similarity_f.pkl','rb'))
# cs_cv = pickle.load(open('cos_similarity.pkl','rb'))
# cs_cv1 = pickle.load(open('cos_similarity.pkl','rb'))
# cs_tfidf = pickle.load(open('cos_similarity.pkl','rb'))
# cs_tfidf = pickle.load(open('cos_similarity.pkl','rb'))
# cs_word2vec = pickle.load(open('cos_similarity.pkl','rb'))

def reccomend(movie, simi=cs_cv_f):
    movie_list= []
    index = new_df[new_df['title']==movie].index[0]
    reccomend_movies = sorted(list(enumerate(simi[index])), reverse= True, key = lambda x: x[1])[1:6]
    for i, recc in reccomend_movies:
        movie_list.append(new_df['title'].iloc[i])
        # print(f"Movies: {new_df['title'].iloc[i]}\t Percentages of Matching: {(recc*100):.2f}%")
    return movie_list, reccomend_movies


st.set_page_config(
    page_title="MovieBuddy 🎬",   # This will appear on the browser tab
    page_icon="🎥",               # Optional: emoji or icon
    layout="centered",            # 'wide' or 'centered'
    initial_sidebar_state="expanded"
)

st.title("Welcome to MovieBuddy 🎬")
st.subheader("Discover movies similar to your favorites!")
movie = st.selectbox("Pick a movie you love… and we’ll find similar ones!", options = ['Your pick 🍿'] + new_df['title'].tolist())
if st.button('Get Movies'):
    movie_list, reccomend_movies = reccomend(movie)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header('Movies')
        for i in range(5):
            st.write(movie_list[i])
    
    with col2:
        st.header('Percentage Match')
        for i,recc in reccomend_movies:
            st.write(f"{(recc*100):.2f}%")