import csv
import os
import tomllib
from collections import UserDict
from pathlib import Path


DATA_DIR = Path(__file__).parent.resolve() / "data"


def get_global(dev_mode):
    """Returns the global context which is available in all templates."""
    dir = DATA_DIR / "global"
    context = make_context("global", dir, toml_files=["global.toml"])

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
    dir = DATA_DIR / "local"

    spots = make_context("spots", dir, csv_files=["spots.csv"]).data
    for spot in spots["spots"]:
        spot["id"] = spot["name"].lower().replace(" ", "-").replace("'", "")

    committee = make_context("committee", dir, csv_files=[
                             "committee_members.csv"]).data

    return [
        ("spots.html", spots),
        ("committee.html", committee)
    ]


def make_context(name, source_dir, toml_files=None, csv_files=None):
    context = Context(name)

    for filename in toml_files or []:
        context.add_from_toml(source_dir / filename)

    for filename in csv_files or []:
        context.add_from_csv(source_dir / filename)

    return context


class Context(UserDict):
    def __init__(self, name, *args, **kwargs):
        self.name = name
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

        with open(filename, newline="") as f:
            lines = f.readlines()
        self.data[entryname] = list(csv.DictReader(lines))

    def add_from_toml(self, filename):
        """Adds the data from the TOML file located in source_dir."""
        with open(filename, "rb") as f:
            data = tomllib.load(f)

        for entryname in data:
            self.warn_if_entry_already_exists(entryname)
            self.data[entryname] = data[entryname]

    def warn_if_entry_already_exists(self, entryname):
        if entryname in self.data:
            print("Warning: Duplicate context data in "
                  f"{self.name}.{entryname}.")
