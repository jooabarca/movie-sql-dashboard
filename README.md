# Movie Ratings Dashboard

An interactive dashboard that analyzes movie ratings using SQL and PostgreSQL, powered by Python and Streamlit.

## Features

- Top-rated movies with 100+ reviews
- Most rated movies overall
- Average rating by genre
- Live PostgreSQL queries displayed in a clean UI
- Genre and year-based filtering
- Export results as CSV

## Tech Stack

- **PostgreSQL** (via Supabase)
- Python (`pandas`, `psycopg2`)
- Streamlit
- Plotly

## How It Works

This dashboard connects directly to a PostgreSQL database hosted on Supabase. It runs raw SQL queries using `psycopg2` to retrieve real-time movie analytics, such as:

- Aggregated ratings
- Genre popularity
- Year-based filtering

PostgreSQL-specific functions (like `ILIKE`, `REGEXP_REPLACE`, and `CAST`)

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py