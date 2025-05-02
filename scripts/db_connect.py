import psycopg2
import pandas as pd

# Replace these with your actual PostgreSQL credentials
DB_NAME = "movies_db"
DB_USER = "postgres"
DB_PASSWORD = "123Momiaes!"
DB_HOST = "localhost"
DB_PORT = "5432"

def run_query(sql):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

        # Run query and return as DataFrame
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df

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