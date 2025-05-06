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

query = f"""
WITH filtered AS (
  SELECT
    m.title,
    m.genres,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(*) AS num_ratings,
    REGEXP_REPLACE(m.title, '.*\\((\\d{{4}})\\)', '\\1')::INTEGER AS year
  FROM ratings r
  JOIN movies m ON r."movieId" = m."movieId"
  WHERE m.title ~ '\\(\\d{{4}}\\)'
  {genre_condition}
  GROUP BY m.title, m.genres
)
SELECT * FROM filtered
WHERE num_ratings >= {min_ratings} AND year >= {min_year}
ORDER BY {order_column} DESC
LIMIT 50;
"""

df = run_query(query)

# --- Metrics ---
if df is not None and not df.empty:
    col1, col2 = st.columns(2)
    col1.metric("🎞️ Movies Shown", len(df))
    col2.metric("⭐ Avg Rating", round(df["avg_rating"].mean(), 2))

# --- Table ---
st.subheader("Results Table")
st.dataframe(df)

# --- Bar Chart ---
if not df.empty:
    st.subheader(f"Top Movies by {sort_by}")
    chart = px.bar(
        df,
        x="title",
        y=order_column,
        color="genres",
        title="Top Movies",
        labels={"title": "Movie Title", order_column: sort_by},
        height=500
    )
    st.plotly_chart(chart, use_container_width=True)
else:
    st.info("No results match your filters.")

# --- Pie Chart ---
if not df.empty:
    st.subheader("Genre Distribution")
    genre_counts = df["genres"].value_counts().reset_index()
    genre_counts.columns = ["genres", "count"]
    pie = px.pie(genre_counts, names="genres", values="count", title="Genres in Result Set")
    st.plotly_chart(pie, use_container_width=True)

# --- CSV Export ---
if not df.empty:
    st.subheader("⬇Export Results")
    st.download_button(
        label="Download table as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="top_movies_filtered.csv",
        mime="text/csv"
    )
