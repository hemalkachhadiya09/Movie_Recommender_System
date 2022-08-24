


import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

option = st.selectbox(
     'Select Type of Recommender System',
     ('Popularity-Based Recommender System', 'Content-Based Recommender System', 'Collaborative Based Recommender System'))



st.title(option)
movie_df=pd.read_csv("movies.csv")
df=pd.read_csv("ratings.csv")

type_movies=movie_df.groupby("genres")["movieId"].sum().sort_values(ascending=False)

merged_left = pd.merge(left=movie_df, right=df, how='left', left_on='movieId', right_on='movieId')

def movie_recommend(original_title):
    idx = indices[original_title]
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return movie_title.iloc[movie_indices]

def recommendMovie(title,topN):
  result=pd.DataFrame(movie_recommend(title).head(topN))
  return result

if option=='Popularity-Based Recommender System':
     ge=st.text_input("Genre(g):","Comedy")
     th=st.text_input("Minimum reviews threshold(t):",100)
     re=st.text_input("Num recommendations (N) :",5)
     out=merged_left[merged_left["genres"]==ge ].sort_values(by=["genres","rating","userId"], ascending=False)
     out=out[out["userId"]>=int(th)]
     out["Num Reviews"]=out.userId.astype("int")
     out["Movie Title"]=out.title
     out["Average Movie Rating"]=out.rating.astype("float")
     out=out.reset_index(drop=True)
     final=out[["Movie Title","Average Movie Rating","Num Reviews"]]
     st.write(final.head(int(re)))
elif option=='Content-Based Recommender System':
    movie_df['genres']=movie_df['genres'].str.replace("|"," ")
    movie_df['title']=movie_df['title'].str.replace('(\(\d\d\d\d\))','')
    movie_df['title']=movie_df['title'].apply(lambda x:x.strip())

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    matrix = tf.fit_transform(movie_df['genres'])
    from sklearn.metrics.pairwise import linear_kernel
    cosine_similarities = linear_kernel(matrix,matrix)
    movie_title = movie_df['title']
    indices = pd.Series(movie_df.index, index=movie_df['title'])
    title=st.text_input("Movie Title (t): ",'Jumanji')
    topN=st.text_input("Num recommendations (N):",5)
    final=recommendMovie(title,int(topN))
    final = final.rename(columns={'title': 'Movie Title'})
    final.index.name='Movie Id'
    final.reset_index(level=0, inplace=True)
    st.write(final)
else:
  st.write(print("nothing"))