import streamlit as st
import pandas as pd
import plotly.express as px
from scripts.db_connect import run_query

st.set_page_config(page_title="🎬 MovieLens Showcase", layout="wide")

st.title("🎬 MovieLens Analytics Dashboard")
st.markdown("""
A simple but powerful movie insights app powered by **PostgreSQL** and **Streamlit**.

We highlight:
- ⭐ Highest Rated Movies (with 100+ votes)
- 🎭 Most Popular Genres by Rating Count
""")

# --- Query 1: Top Rated Movies ---
query_top_movies = """
SELECT
    m.title,
    m.genres,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(*) AS num_ratings
FROM ratings r
JOIN movies m ON r."movieId" = m."movieId"
GROUP BY m.title, m.genres
HAVING COUNT(*) >= 100
ORDER BY avg_rating DESC
LIMIT 10;
"""
df_movies = run_query(query_top_movies)

# --- Query 2: Most Rated Genres ---
query_top_genres = """
SELECT
    m.genres,
    COUNT(*) AS total_ratings
FROM ratings r
JOIN movies m ON r."movieId" = m."movieId"
GROUP BY m.genres
ORDER BY total_ratings DESC
LIMIT 10;
"""
df_genres = run_query(query_top_genres)

# --- Display Results ---
st.header("⭐ Top 10 Highest Rated Movies")
if df_movies is not None and not df_movies.empty:
    st.dataframe(df_movies)
    fig1 = px.bar(df_movies, x="title", y="avg_rating", color="genres",
                  title="Top Rated Movies", labels={"avg_rating": "Average Rating"})
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("No movie data available.")

st.header("🎭 Top 10 Most Rated Genres")
if df_genres is not None and not df_genres.empty:
    st.dataframe(df_genres)
    fig2 = px.pie(df_genres, names="genres", values="total_ratings",
                  title="Most Popular Genres")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No genre data available.")
