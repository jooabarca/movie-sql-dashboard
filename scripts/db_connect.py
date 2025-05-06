import pandas as pd
import psycopg2
import streamlit as st

def run_query(sql):
    try:
        conn = psycopg2.connect(st.secrets["DB_URL"])
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Query failed: {e}")
        return None

    except Exception as e:
        print("Error:", e)
        return None

# Example usage
if __name__ == "__main__":
    query = """
    SELECT m.title, ROUND(AVG(r.rating), 2) AS avg_rating, COUNT(*) AS num_ratings
    FROM ratings r
    JOIN movies m ON r.movieId = m.movieId
    GROUP BY m.title
    HAVING COUNT(*) >= 100
    ORDER BY avg_rating DESC
    LIMIT 10;
    """
    df = run_query(query)
    print(df)