import csv
import os
from pathlib import Path


DATA_DIR = Path(__file__).parent.resolve() / "data"


def get_global():
    """Returns the global context which is available in all templates."""
    dir = DATA_DIR / "global"
    global_context = Context("global", dir)

    for filename in os.listdir(dir):
        if filename.endswith(".csv"):
            global_context.add_from_csv(filename)

    return global_context.data


class Context:
    def __init__(self, name, source_dir):
        self.data = dict()
        self.name = name
        self.source_dir = source_dir

    def path_from_filename(self, filename):
        return self.source_dir / filename

    def add_from_csv(self, filename, entryname=None):
        """
        Adds the data from the CSV file located in source_dir and assigns it
        the given entryname.

        If entryname is omitted, uses filename, without the extension.
        """
        if entryname is None:
            basename = os.path.basename(filename)
            entryname = os.path.splitext(basename)[0]

        if entryname in self.data:
            print("Warning: Duplicate context data in "
                  f"{self.name}.{entryname}.")

        with open(self.path_from_filename(filename), newline="") as f:
            lines = f.readlines()
        self.data[entryname] = list(csv.DictReader(lines))
