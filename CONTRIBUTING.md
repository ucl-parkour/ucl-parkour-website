# Contributing

This project is built using the [jinja] templating system with [staticjinja].

[jinja]: https://jinja.palletsprojects.com/en/stable/
[staticjinja]: https://github.com/staticjinja/staticjinja

## Setup

After cloning the repository, set up [Poetry] and run the build script:

```bash
cd ucl-parkour-website
poetry sync
# See the Poetry docs for how to activate the virtual environment in your shell.
eval $(poetry env activate)
python -m build_dev
```

The script will build the website and place the files in `/build`. It will
watch the `/src/templates` directory for changes and update the built files as
needed.

### Serving the site

To serve the site locally with hot-reloading, use something like [live-server]:

```bash
live-server build
```

[Poetry]: https://python-poetry.org/
[live-server]: https://www.npmjs.com/package/live-server

## Making changes

For most changes, you just need to add a new html document in `/src/templates`.
You should be familiar with the [template designer docs].

[template designer docs]: https://jinja.palletsprojects.com/en/stable/templates/

### Context data

To add context data, you can add a file to `/src/data` and register it in
`/src/context.py`. There are helper functions for importing data from csv and
toml files.

See the [relevant entry] in the staticjinja docs for more information.

[relevant entry]: https://staticjinja.github.io/staticjinja/user/advanced.html#loading-data

### Conventions

- Use the `club` global context variable to store details about the club that
  is subject to change and/or often repeated.
- Use the `pages` global context variable to link to other pages on the site. Add
  to this variable when creating a new page.
- Use [BEM] when writing CSS.

[BEM]: https://getbem.com/introduction/
