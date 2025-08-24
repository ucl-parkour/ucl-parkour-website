from staticjinja import Site

from . import context


def render(use_reloader=False):
    site = Site.make_site(
        searchpath="src/templates",
        outpath="build",
        staticpaths=["./css/", "./img/", "./fonts/"],
        env_globals=context.get_global(),
    )
    site.render(use_reloader=use_reloader)
