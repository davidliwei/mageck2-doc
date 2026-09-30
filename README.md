# mageck2-doc

The documentation source for [MAGeCK2](https://github.com/davidliwei/mageck2), a
model-based analysis tool for CRISPR screens from the
[Wei Li lab](https://weililab.org).

**📖 Read the documentation at [mageck2.readthedocs.io](https://mageck2.readthedocs.io).**

## Contents

The pages are MyST Markdown, so they are readable here on GitHub as well as on
the rendered site:

| Page | |
|---|---|
| [docs/INSTALL.md](docs/INSTALL.md) | Installation |
| [docs/TUTORIAL.md](docs/TUTORIAL.md) | Step-by-step walkthroughs |
| [docs/usage/](docs/usage/) | Command-line reference |
| [docs/FILE_FORMATS.md](docs/FILE_FORMATS.md) | Input and output file specifications |
| [docs/FAQ.md](docs/FAQ.md) | Frequently asked questions |

The command-line reference is **generated** from MAGeCK2's own argument parser by
[sphinx-argparse](https://sphinx-argparse.readthedocs.io/) when the site is
built, so it cannot fall behind the software. The pages under `docs/usage/` hold
only the surrounding prose; the option tables appear when the site is built and
are not checked in. To change what an option's description says, change its
`help=` string in
[`mageck2/argsParser.py`](https://github.com/davidliwei/mageck2/blob/main/mageck2/argsParser.py).

## Building locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r docs/requirements.txt
sphinx-build -W --keep-going -b html docs docs/_build/html
open docs/_build/html/index.html
```

`docs/requirements.txt` installs MAGeCK2 from its `main` branch, because the
build imports it to read the parser. `-W` turns warnings into errors, which is
what CI and Read the Docs both do — an unresolved cross-reference is treated as a
build failure rather than a silently broken link.

## Related repositories

* [mageck2](https://github.com/davidliwei/mageck2) — source code and issue tracker
* [mageck2-demo](https://github.com/davidliwei/mageck2-demo) — runnable example datasets and workflows

## License

This documentation is released under the [BSD 3-Clause License](LICENSE), the
same license as MAGeCK2.
