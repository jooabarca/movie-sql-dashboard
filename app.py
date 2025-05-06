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

# --- Sidebar filters ---
st.sidebar.header("🔎 Explore the Data")
min_votes = st.sidebar.slider("Minimum number of ratings", 10, 500, 100, step=10)
sort_by = st.sidebar.selectbox("Sort movies by", ["Average Rating", "Number of Ratings"])
genre_filter = st.sidebar.selectbox("Filter by Genre", ["All", "Action", "Comedy", "Drama", "Horror", "Romance", "Thriller"])
min_year = st.sidebar.slider("Minimum release year", 1950, 2025, 2000)

order_column = "avg_rating" if sort_by == "Average Rating" else "num_ratings"

# --- Genre condition ---
genre_condition = ""
if genre_filter != "All":
    genre_condition = f"AND m.genres ILIKE '%%{genre_filter}%%'"

# --- Query 1: Top Rated Movies ---
query_top_movies = f"""
WITH filtered AS (
    SELECT
        m.title,
        m.genres,
        ROUND(AVG(r.rating), 2) AS avg_rating,
        COUNT(*) AS num_ratings,
        CASE 
            WHEN m.title ~ '\\(\\d{{4}}\\)$' THEN REGEXP_REPLACE(m.title, '.*\\((\\d{{4}})\\)$', '\\1')::INTEGER
            ELSE NULL
        END AS year
    FROM ratings r
    JOIN movies m ON r."movieId" = m."movieId"
    WHERE 1=1
    {genre_condition}
    GROUP BY m.title, m.genres, m.title
)
SELECT * FROM filtered
WHERE num_ratings >= {min_votes} AND year IS NOT NULL AND year >= {min_year}
ORDER BY {order_column} DESC
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
    fig1 = px.bar(df_movies, x="title", y=order_column, color="genres",
                  title=f"Top Movies by {sort_by}", labels={order_column: sort_by})
    st.plotly_chart(fig1, use_container_width=True)

    st.download_button(
        label="⬇ Download Movies CSV",
        data=df_movies.to_csv(index=False).encode("utf-8"),
        file_name="top_movies.csv",
        mime="text/csv"
    )
else:
    st.warning("No movie data available.")

st.header("🎭 Top 10 Most Rated Genres")
if df_genres is not None and not df_genres.empty:
    st.dataframe(df_genres)
    fig2 = px.pie(df_genres, names="genres", values="total_ratings",
                  title="Most Popular Genres")
    st.plotly_chart(fig2, use_container_width=True)

    st.download_button(
        label="⬇ Download Genres CSV",
        data=df_genres.to_csv(index=False).encode("utf-8"),
        file_name="top_genres.csv",
        mime="text/csv"
    )
else:
    st.warning("No genre data available.")
