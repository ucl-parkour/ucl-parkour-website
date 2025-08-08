# UCL Parkour Club Website

## Usage

After cloning, set up [Poetry] and run the build script:

```bash
poetry sync
# See the Poetry docs for how to activate the virtual environment in your shell.
eval $(poetry env activate)
python -m build_dev
```

To serve the site locally, use something like [live-server]:

```bash
live-server build
```

[Poetry]: https://python-poetry.org/
[live-server]: https://www.npmjs.com/package/live-server
