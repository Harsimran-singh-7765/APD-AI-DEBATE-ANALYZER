# patch.py
import os
os.environ["CREWAI_DISABLE_MEMORY"] = "1"
os.environ["CHROMA_DB_IMPL"] = "duckdb"  # Force it off sqlite

# Optional safety (not strictly needed, but helps in some builds)
import chromadb
chromadb.config.Settings().is_persistent = False
