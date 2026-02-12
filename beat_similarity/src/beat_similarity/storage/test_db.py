"""
Basic connection test for PostgreSQL and pgvector.
Verifies if the database is reachable and the vector extension is active.
"""

import psycopg2
from pgvector.psycopg2 import register_vector
import sys
import os
from dotenv import load_dotenv

# Add the project root to sys.path for logging utility
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from beat_similarity.src.beat_similarity.utils.logger import setup_app_logger


def test_connection():
    # Set up session-based logger
    logger = setup_app_logger("DB_Test", log_to_session=True)

    # Database configuration (Match your Docker settings)
    db_config = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": os.getenv("DB_PORT")
    }

    conn = None
    try:
        logger.info("Attempting to connect to PostgreSQL...")
        conn = psycopg2.connect(**db_config)

        # Register pgvector to handle VECTOR type in Python
        register_vector(conn)
        logger.info("Connection successful! pgvector is registered.")

        with conn.cursor() as cur:
            # Check if the table we created exists
            cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'beat_features');")
            exists = cur.fetchone()[0]

            if exists:
                logger.info("Table 'beat_features' found. Database is ready for Step 3-3.")
            else:
                logger.warning("Connection OK, but 'beat_features' table is missing. Run the SQL commands first.")

    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")


if __name__ == "__main__":
    test_connection()