"""
Database handler for storing and searching beat embeddings.
This class manages connections using .env config and performs vector searches.
"""

import psycopg2
import os
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector
from beat_similarity.src.beat_similarity.utils.logger import setup_app_logger

class BeatDatabaseHandler:
    def __init__(self, logger):
        self.logger = logger
        load_dotenv()
        self.db_config = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": os.getenv("DB_PORT")
        }
        self.conn = None
        self._connect()

    def _connect(self):
        """Establish connection and register pgvector."""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            register_vector(self.conn)
            self.logger.info("[Database] Connected to PostgreSQL and registered pgvector.")
        except Exception as e:
            self.logger.error(f"[Database] Connection failed: {str(e)}")
            raise

    def save_beat(self, youtube_id, title, bpm, embedding):
        """Insert beat features into the database."""
        try:
            with self.conn.cursor() as cur:
                sql = """
                INSERT INTO beat_features (youtube_id, title, bpm, embedding)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (youtube_id) DO NOTHING;
                """
                # Note: pgvector expects a numpy array or list
                cur.execute(sql, (youtube_id, title, bpm, embedding[0]))
            self.conn.commit()
            self.logger.info(f"[Database] Successfully saved beat: {title}")
        except Exception as e:
            self.conn.rollback()
            self.logger.error(f"[Database] Save failed for {youtube_id}: {str(e)}")

    def search_similar(self, target_embedding, limit=3):
        """Search for the most similar beats using cosine distance (<=>)."""
        try:
            with self.conn.cursor() as cur:
                # 1 - (A <=> B) results in Cosine Similarity
                sql = """
                SELECT youtube_id, title, bpm, 1 - (embedding <=> %s) AS similarity
                FROM beat_features
                ORDER BY similarity DESC
                LIMIT %s;
                """
                cur.execute(sql, (target_embedding[0], limit))
                return cur.fetchall()
        except Exception as e:
            self.logger.error(f"[Database] Search failed: {str(e)}")
            return []

    def close(self):
        if self.conn:
            self.conn.close()
            self.logger.info("[Database] Connection closed.")
