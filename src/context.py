import tomllib
from pathlib import Path


DATA_DIR = Path(__file__).parent.resolve() / "data"


def get_global(dev_mode):
    """Returns the global context which is available in all templates."""
    main = load_context_data("main")

    header_pages = list()
    for id in main["header_page_ids"]:
        header_pages.append(main["pages"][id])
    main["header_pages"] = header_pages

    if dev_mode:
        # GitHub pages handles the missing .html extension but local-server
        # does not.
        for id, page in main["pages"].items():
            if id != "home":
                page["url"] += ".html"

        # Use relative URLs during local development.
        main["club"]["domain_name"] = ""

    spots = load_context_data("spots")
    for spot in spots["spots"]:
        spot["id"] = spot["name"].lower().replace(" ", "-").replace("'", "")

    committee = load_context_data("committee_members")

    return main | spots | committee


def load_context_data(name):
    path = DATA_DIR / f"{name}.toml"
    with open(path, "rb") as f:
        return tomllib.load(f)
