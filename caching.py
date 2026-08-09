import os

from joblib import Memory

memory = Memory(
    None if os.getenv("ENV", "development") == "development" else "./__cache__",
    verbose=1,
)
