import tomllib
from collections import UserDict
from pathlib import Path


DATA_DIR = Path(__file__).parent.resolve() / "data"


def get_global(dev_mode):
    """Returns the global context which is available in all templates."""
    dir = DATA_DIR / "global"
    context = Context("global", dir)

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

        # Use relative URLs during local development.
        context["club"]["domain_name"] = ""
    return context


def get_local():
    """Returns the local context which is available in specific templates."""
    dir = DATA_DIR / "local"

    spots = Context("spots", dir).data
    for spot in spots["spots"]:
        spot["id"] = spot["name"].lower().replace(" ", "-").replace("'", "")

    committee = Context("committee_members", dir).data

    return [
        ("spots.html", spots),
        ("committee.html", committee)
    ]


class Context(UserDict):
    def __init__(self, name, source_dir, *args, **kwargs):
        self.name = name
        self.source_dir = source_dir
        super().__init__(*args, **kwargs)
        self.add_from_toml(f"{name}.toml")

    def add_from_toml(self, filename):
        """Adds the data from the TOML file located in source_dir."""
        with open(self.source_dir / filename, "rb") as f:
            data = tomllib.load(f)

        for entryname in data:
            self.warn_if_entry_already_exists(entryname)
            self.data[entryname] = data[entryname]

    def warn_if_entry_already_exists(self, entryname):
        if entryname in self.data:
            print("Warning: Duplicate context data in "
                  f"{self.name}.{entryname}.")
