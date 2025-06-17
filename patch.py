# crewai_patch.py
import os
os.environ["CREWAI_DISABLE_MEMORY"] = "1"
os.environ["CHROMA_DB_IMPL"] = "duckdb"

import builtins
real_import = builtins.__import__

def safe_import(name, *args, **kwargs):
    if name.startswith("chromadb"):
        raise ImportError("ChromaDB disabled")
    return real_import(name, *args, **kwargs)

builtins.__import__ = safe_import
