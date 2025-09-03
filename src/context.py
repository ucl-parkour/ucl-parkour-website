import csv
import os
import tomllib
from pathlib import Path


DATA_DIR = Path(__file__).parent.resolve() / "data"


def get_global(dev_mode):
    """Returns the global context which is available in all templates."""
    dir = DATA_DIR / "global"
    global_context = Context("global", dir)
    data = global_context.data

    global_context.add_from_toml("global.toml")

    data["header_pages"] = list()
    for id in global_context.data["header_page_ids"]:
        data["header_pages"].append(data["pages"][id])

    if dev_mode:
        # GitHub pages handles the missing .html extension but local-server
        # does not.
        for id, page in data["pages"].items():
            if id != "home":
                page["url"] += ".html"

        data["club"]["domain_name"] = ""
    return data


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

    make_context("committee.html").add_from_csv("committee_members.csv")
    return local_contexts


class Context:
    def __init__(self, name, source_dir):
        self.data = dict()
        self.name = name
        self.source_dir = source_dir

    def add_from_csv(self, filename):
        """
        Adds the data from the CSV file located in source_dir and assigns it
        the given entryname.

        If entryname is omitted, uses filename, without the extension.
        """
        basename = os.path.basename(filename)
        entryname = os.path.splitext(basename)[0]
        self.warn_if_entry_already_exists(entryname)

        with open(self.path_from_filename(filename), newline="") as f:
            lines = f.readlines()
        self.data[entryname] = list(csv.DictReader(lines))

    def add_from_toml(self, filename):
        """Adds the data from the TOML file located in source_dir."""
        with open(self.path_from_filename(filename), "rb") as f:
            data = tomllib.load(f)

        for entryname in data:
            self.warn_if_entry_already_exists(entryname)
            self.data[entryname] = data[entryname]

    def warn_if_entry_already_exists(self, entryname):
        if entryname in self.data:
            print("Warning: Duplicate context data in "
                  f"{self.name}.{entryname}.")

    def path_from_filename(self, filename):
        return self.source_dir / filename
