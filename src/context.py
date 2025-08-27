import csv
import os
from pathlib import Path


DATA_DIR = Path(__file__).parent.resolve() / "data"


def get_global(dev_mode):
    """Returns the global context which is available in all templates."""
    dir = DATA_DIR / "global"
    global_context = Context("global", dir)

    for filename in os.listdir(dir):
        if filename.endswith(".csv"):
            global_context.add_from_csv(filename)

    if dev_mode:
        # GitHub pages handles the missing .html extension but local-server
        # local-server does not.
        for item in global_context.data["header_items"]:
            item["url"] += ".html"
    return global_context.data


def get_local():
    """Returns the local context which is available in specific templates."""
    local_contexts = list()
    dir = DATA_DIR / "local"

    def make_context(name, regex=None):
        """
        Create a context with the given name and make it available to templates
        matching the regex.

        If regex is omitted, uses name instead.
        """
        context = Context(name, dir)
        local_contexts.append((regex or name, context.data))
        return context

    spots = make_context("spots.html")
    spots.add_from_csv("spots.csv")
    for spot in spots.data["spots"]:
        spot["id"] = spot["name"].lower().replace(" ", "-").replace("'", "")
    return local_contexts


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
