from staticjinja import Site

from . import context


def render(dev_mode=False):
    site = Site.make_site(
        searchpath="src/templates",
        outpath="build",
        staticpaths=["./css/", "./img/", "./fonts/"],
        env_globals=context.get_global(dev_mode),
        contexts=context.get_local(),
    )
    site.render(use_reloader=dev_mode)
