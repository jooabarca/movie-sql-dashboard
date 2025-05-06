import streamlit as st
from scripts.db_connect import run_query
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="MovieLens Dashboard", layout="wide")

st.title("MovieLens Dashboard + PostgreSQL + Streamlit")
st.markdown("Analyze movie ratings with real time SQL queries, genre filtering, year range, and interactive charts.")

# --- Sidebar filters ---
st.sidebar.header("🔎 Filters")

min_ratings = st.sidebar.slider("Minimum number of ratings:", 10, 1000, 100, 10)

sort_by = st.sidebar.selectbox(
    "Sort by:",
    options=["Average Rating", "Number of Ratings"]
)

genre_filter = st.sidebar.selectbox(
    "Genre contains:",
    options=["All", "Action", "Comedy", "Drama", "Horror", "Romance", "Thriller"]
)

min_year = st.sidebar.slider("Minimum release year:", 1950, 2025, 2000)

# --- Build SQL Query ---
order_column = "avg_rating" if sort_by == "Average Rating" else "num_ratings"

genre_condition = ""
if genre_filter != "All":
    genre_condition = f"AND m.genres ILIKE '%{genre_filter}%'"

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

df_movies = run_query(query_top_movies)
df_genres = run_query(query_top_genres)

