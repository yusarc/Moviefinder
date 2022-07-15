import streamlit as st
import pandas as pd
from pathlib import Path

header=st.container()
dataset=st.container()
features=st.container()
model_training=st.container()



with header:
    st.title('WBSFLIX')
    st.text("***Movie Recommender***")

with dataset:
    st.header("Ratings Dataset")
    st.text("Uploading...")
    
    ratings= Path("OneDrive/Desktop/WBS_Coding/8.Recommender System/ml-latest-small/ratings.csv").parents[1]/"ml-latest-small/ratings.csv"
    ratings= pd.read_csv('https://raw.githubusercontent.com/yusarc/moviefinder/master/ratings.csv')
    st.write(ratings.head(10))
    
    st.subheader("Distrubiton of Ratings")
    ratings_spread=pd.DataFrame(ratings['rating'].value_counts()).head(20)
    st.bar_chart(ratings_spread)
    
    st.header("Movies Dataset")
    st.text("Uploading...")
    
    movies=Path("OneDrive/Desktop/WBS_Coding/8.Recommender System/ml-latest-small/movies.csv").parents[1]/"ml-latest-small/movies.csv"
    movies= pd.read_csv('https://raw.githubusercontent.com/yusarc/moviefinder/master/movies.csv')
    st.write( movies.head(10))
    
    st.subheader("Distrubiton of Genres")
    genres_spread=pd.DataFrame(movies['genres'].value_counts()).head(20)
    st.bar_chart(genres_spread)
    
with features:
    st.header('Which movie is the best?')
    
    st.markdown("* Just choose one of the movies' Id from datasets that you like, and we will list top similar movies for you!") 
    
with model_training:
    st.header('Moviefinder')
    st.text("Let's get start it...")
    
    sel_col, disp_col = st.columns(2)
    movie_id= sel_col.selectbox("Just give me movie's Id", options=[1,2,3,4,5,6,7,8,9,10],index=0)
    n= sel_col.selectbox("How many movie do you want to list?", options=[1,2,3,4,5,6,7,8,9,10],index=0)
    
#     title = sel_col.selectbox("Just give me movie's Id", options=['Toy Story (1995)','Jumanji (1995)','Grumpier Old Men (1995)'],index=0)
#     movieId = movies.loc[movies.title == title]['movieId']
    
    def top_n_mov(movie_id, n):
    
             ratings_crosstab=pd.pivot_table(data=ratings, values='rating',          index='userId', columns='movieId')
    
    # pick ratings given to the inputed movies
             mov_ratings = ratings_crosstab[movie_id]
    
    # Calc the correlations between the inputed movie and the rest
             similar_to_mov = ratings_crosstab.corrwith(mov_ratings)
    
    # drop missing values
             corr_mov = pd.DataFrame(similar_to_mov, columns=['PearsonR'])
             corr_mov.dropna(inplace=True)
    
    #create a new df with rating_count
             mov_rating_count = pd.DataFrame(ratings.groupby('movieId')['rating'].mean())
             mov_rating_count['rating_count'] = ratings.groupby('movieId')['rating'].count()
    
    # join corr coeffiecients with rating counts
             mov_corr_summary = corr_mov.join(mov_rating_count['rating_count'])
             mov_corr_summary.drop(movie_id, inplace=True) # drop the inputed movie itself
    
    #filter movies with less than 50 rating_count and pick the top n
             top10 = mov_corr_summary[mov_corr_summary['rating_count']>=50].sort_values('PearsonR', ascending=False).head(n)
    
    # merge with places to get the movie titles
             top10 = top10.merge(movies, left_index=True, right_on="movieId")
    
             return list(top10["title"])
    
    disp_col.subheader(" Check it out!")
    disp_col.write(top_n_mov(movie_id, n))
    
    
     
 

