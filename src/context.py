import tomllib
from pathlib import Path


DATA_DIR = Path(__file__).parent.resolve() / "data"


def get_global(dev_mode):
    """Returns the global context which is available in all templates."""
    dir = DATA_DIR / "global"
    context = load_context_data(dir / "global.toml")

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

    spots = load_context_data(dir / "spots.toml")
    for spot in spots["spots"]:
        spot["id"] = spot["name"].lower().replace(" ", "-").replace("'", "")

    committee = load_context_data(dir / "committee_members.toml")

    return [
        ("spots.html", spots),
        ("committee.html", committee)
    ]


def load_context_data(path):
    with open(path, "rb") as f:
        return tomllib.load(f)
