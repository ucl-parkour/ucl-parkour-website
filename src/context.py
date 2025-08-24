import csv
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.resolve() / "data"


def get_global():
    """Returns the global context which is available in all templates."""
    global_context = dict()
    dir = DATA_DIR / "global"
    for path, entry_name in _get_datafiles(dir):
        with open(path, newline="") as f:
            entry_data = list(csv.DictReader(f.readlines()))
            global_context[entry_name] = entry_data

    return global_context


def _get_datafiles(dir):
    """
    Yields valid data files in dir as tuples containing the full file path
    and the base file name.
    """
    for file in os.listdir(dir):
        file_name = os.fsdecode(file)
        entry_name, ext = os.path.splitext(file_name)
        if ext == ".csv":
            yield dir / file_name, entry_name
