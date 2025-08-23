from staticjinja import Site


def render(use_reloader=False):
    site = Site.make_site(
        searchpath="src/templates",
        outpath="build",
        staticpaths=["./css/", "./img/", "./fonts/"],
        env_globals={
            "header_items": [
                "Skills",
                "Spot map",
                "Gallery",
                "Committee",
                "Contact us",
            ],
        },
    )
    site.render(use_reloader=use_reloader)
