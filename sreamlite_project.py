
import streamlit as st
import pandas as pd
import numpy as np

option = st.selectbox(
    'Select Type of Recommender System',
    ('Popularity-Based Recommender System', 'Content-Based Recommender System',
     'Collaborative Based Recommender System'))

st.title(option)
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
type_movies = movies.groupby("genres")["movieId"].sum().sort_values(ascending=False)
# st.write("List of Genres")
# st.write(type_movies.drop(columns="movieId"))
# title= st.text_input('Movie title', 'Life of Brian')
# st.write('The current movie title is', title)


merged_left = pd.merge(left=movies, right=ratings, how='left', left_on='movieId', right_on='movieId')
if option == 'Popularity-Based Recommender System':
    ge = st.text_input("Genre(g):", "Comedy")
    th = st.text_input("Minimum reviews threshold(t):", 100)
    re = st.text_input("Num recommendations (N) :", 5)
    out = merged_left[merged_left["genres"] == ge].sort_values(by=["genres", "rating", "userId"], ascending=False)
    out = out[out["userId"] >= int(th)]
    out["Num Reviews"] = out.userId.astype("int")
    out["Movie Title"] = out.title
    out["Average Movie Rating"] = out.rating.astype("float")
    out = out.reset_index(drop=True)
    final = out[["Movie Title", "Average Movie Rating", "Num Reviews"]]
    st.write(final.head(int(re)))
elif option == 'Content-Based Recommender System':
    for i in range(0, len(movies)):
        Str = movies["title"][i]
        l = len(Str)
        Remove_last = Str[:l - 7]
        movies["title"][i] = Remove_last
    n_movies = movies
    mv = st.text_input("Movie Title (t): ", 'Jumanji')
    rec = st.text_input("Num recommendations (N):", 5)
    movie = n_movies[n_movies["title"] == mv]

    id1 = movie["movieId"].tolist()
    id2 = id1[0]
    genre = merged_left[merged_left["movieId"] == id2]
    genre = genre["genres"].unique()
    gen = genre.tolist()
    ge = gen[0]
    out2 = merged_left[merged_left["genres"] == ge].sort_values(by=["genres", "rating", "userId"], ascending=False)
    out2 = out2.reset_index(drop=True).title.head(int(rec))
    st.write(out2)
else:
    usr = st.text_input("UserID:", 1)
    rec = st.text_input("Num recommendations(N):", 10)
    thr = st.text_input("Threshold for similar users (k):", 100)
    usr_mv = merged_left[merged_left["userId"] == int(usr)][["title", "userId"]]
    a = usr_mv.title.tolist()
    diff_usr = merged_left[merged_left["title"] == a[0]]
    for i in range(1, len(a)):
        diff_usr = diff_usr.append(merged_left[merged_left["title"] == a[i]])
    diff_usr = diff_usr["userId"].unique()
    diff_usr = diff_usr.tolist()
    diff_usr = diff_usr[:int(thr)]
    sg_mv = merged_left[merged_left["userId"] == diff_usr[0]]
    for i in range(1, len(diff_usr)):
        sg_mv = sg_mv.append(merged_left[merged_left["userId"] == diff_usr[i]])
    sg_mv = sg_mv.reset_index(drop=True)
    sg_mv = sg_mv["title"].unique()
    sg_mv = pd.DataFrame(sg_mv, columns=["Movie Title"])
    st.write(sg_mv.head(int(rec)))