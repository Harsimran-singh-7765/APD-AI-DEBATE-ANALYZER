# crewai_patch.py
import os
os.environ["CREWAI_DISABLE_MEMORY"] = "1"
os.environ["CHROMA_DB_IMPL"] = "duckdb"

# Monkey patch Chroma import if still triggered
import builtins
builtins.__dict__["__import__"] = lambda name, *args, **kwargs: (
    None if name.startswith("chromadb") else __import__(name, *args, **kwargs)
)
