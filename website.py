from staticjinja import Site


def render(use_reloader=False):
    site = Site.make_site(
        outpath="./build/",
        staticpaths=["./css/", "./img/", "./fonts/"]
    )
    site.render(use_reloader=use_reloader)
