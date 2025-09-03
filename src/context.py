import csv
import os
import tomllib
from collections import UserDict
from pathlib import Path


DATA_DIR = Path(__file__).parent.resolve() / "data"


def get_global(dev_mode):
    """Returns the global context which is available in all templates."""
    dir = DATA_DIR / "global"
    context = Context("global", dir)

    context.add_from_toml("global.toml")

    header_pages = list()
    for id in context["header_page_ids"]:
        header_pages.append(context["pages"][id])
    context["header_pages"] = header_pages

    if dev_mode:
        # GitHub pages handles the missing .html extension but local-server
        # does not.
        for id, page in context["pages"].items():
            if id != "home":
                page["url"] += ".html"

        context["club"]["domain_name"] = ""
    return context


def get_local():
    """Returns the local context which is available in specific templates."""
    contexts = list()
    dir = DATA_DIR / "local"

    def make_context(name, regex=None):
        """
        Create a context with the given name and make it available to templates
        matching the regex.

        If regex is omitted, uses name instead.
        """
        context = Context(name, dir)
        contexts.append((regex or name, context.data))
        return context

    spots = make_context("spots.html")
    spots.add_from_csv("spots.csv")
    for spot in spots["spots"]:
        spot["id"] = spot["name"].lower().replace(" ", "-").replace("'", "")

    make_context("committee.html").add_from_csv("committee_members.csv")
    return contexts


class Context(UserDict):
    def __init__(self, name, source_dir, *args, **kwargs):
        self.name = name
        self.source_dir = source_dir
        super().__init__(*args, **kwargs)

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
