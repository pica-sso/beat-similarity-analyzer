"""
Main Application Controller.
Includes logic to build a library (Ingestion) and search for similarities.
"""

import os
import sys

# Ensure the project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from beat_similarity.utils.logger import setup_app_logger
from beat_similarity.ingestion.youtube import YouTubeDownloader
from beat_similarity.feature.extractor import BeatFeatureExtractor
from beat_similarity.storage.database import BeatDatabaseHandler

def process_and_save(url, title, bpm, logger, db_handler, extractor, downloader):
    """Workflow: Download -> Extract -> Save to DB (If not exists)"""
    try:
        youtube_id = url.split("v=")[-1]

        # Checking if already exists in DB to save time/bandwidth
        logger.info(f"Checking if beat exists in DB: {title} ({youtube_id})")

        # (Optional: You can add a 'check_exists' method in database.py later)
        # For now, we rely on ON CONFLICT DO NOTHING in SQL.

        path = downloader.download(url, f"temp_{youtube_id}")
        vector = extractor.extract_vector(path)
        db_handler.save_beat(youtube_id, title, bpm, vector)

        if os.path.exists(path):
            os.remove(path)

    except Exception as e:
        logger.error(f"Failed to process {title}: {str(e)}")

def run_app(target_url):
    """
    Main logic:
    1. Ingest baseline beats into DB.
    2. Search for the target_url within the DB.
    """
    logger = setup_app_logger("BeatSimilarityApp", log_to_session=True)
    db = BeatDatabaseHandler(logger)
    extractor = BeatFeatureExtractor(logger)
    downloader = YouTubeDownloader(logger, download_path="temp_files")

    try:
        # --- PHASE 1: Build your Library (Ingestion) ---
        # Add real YouTube links you want to keep in your DB.
        library_beats = [
            {"url": "https://www.youtube.com/watch?v=BrxZ7PsPMY0", "title": "Trap Beat A", "bpm": 156.0},
            {"url": "https://www.youtube.com/watch?v=0OEERL7u9jo", "title": "Old School Beat B", "bpm": 90.0}
        ]

        for beat in library_beats:
            process_and_save(beat['url'], beat['title'], beat['bpm'], logger, db, extractor, downloader)

        # --- PHASE 2: Search for Similarity ---
        logger.info(f"--- Starting Similarity Search for Target: {target_url} ---")

        # 1. Download and get vector for the test target (Do not save to DB)
        test_path = downloader.download(target_url, "search_target")
        test_vector = extractor.extract_vector(test_path)

        # 2. Query the Database
        results = db.search_similar(test_vector, limit=5)

        # 3. Print Results
        print("\n" + "★"*50)
        print(" SEARCH RESULTS (Top Matches in DB) ")
        print("★"*50)
        if not results:
            print("No similar beats found in the database.")
        for i, res in enumerate(results, 1):
            # res: (youtube_id, title, bpm, similarity)
            print(f"{i}. [{res[1]}] | Similarity: {res[3]*100:.2f}% | BPM: {res[2]}")
        print("★"*50 + "\n")

    except Exception as e:
        logger.error(f"Application crash: {str(e)}")
    finally:
        # Final cleanup
        if os.path.exists("temp_files/search_target.wav"):
            os.remove("temp_files/search_target.wav")
        db.close()

if __name__ == "__main__":
    # REPLACE THIS with a real YouTube URL you want to test!
    # Try a beat that is similar to Trap Beat A or Old School Beat B.
    MY_TEST_URL = "https://www.youtube.com/watch?v=vshq_Xur6-E&list=RDvshq_Xur6-E&start_radio=1"

    run_app(MY_TEST_URL)