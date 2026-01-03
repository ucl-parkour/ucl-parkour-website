import tomllib
from pathlib import Path


DATA_DIR = Path(__file__).parent.resolve() / "data"


def get_global(dev_mode):
    """Returns the global context which is available in all templates."""
    main = load_context_data("main")
    main["header_pages"] = [main["pages"][id]
                            for id in main["header_page_ids"]]

    spots = load_context_data("spots")
    for spot in spots["spots"]:
        spot["id"] = slugify(spot["name"])

    committee = load_context_data("committee", as_subtable=True)
    committee["committee"]["all_positions_filled"] = all(
        "incumbent" in pos.keys() for pos in committee["committee"]["positions"])

    if dev_mode:
        # We miss the .html extension in URLs because this looks better, and
        # GitHub Pages handles this correctly. In development, we may be using
        # tools such as local-server, which do not handle this correctly.
        # So we add the extension to the URLs.
        pages = (page for page in main["pages"].values() if page["url"] != "/")
        for page in pages:
            page["url"] += ".html"

    merged_context = main | spots | committee
    return merged_context


def load_context_data(name, as_subtable=False):
    """
    Loads the TOML file from the data directory called {name}.toml.

    If as_subtable is given, nests the result in a dictionary under the key
    {name}.
    """
    path = DATA_DIR / f"{name}.toml"
    with open(path, "rb") as f:
        data = tomllib.load(f)

    if as_subtable:
        return {name: data}
    return data


def slugify(name):
    """
    Converts a name into a URL slug.

    For example, "Abbey Road" becomes "abbey-road".
    """
    return name.lower().replace(" ", "-").replace("'", "")
