"""Sphinx configuration for the MAGeCK2 documentation.

The pages are MyST Markdown so they stay readable on GitHub, and the
command-line reference under ``usage/`` is generated from MAGeCK2's own argument
parser by ``sphinx-argparse``. That means this build imports ``mageck2``:
``docs/requirements.txt`` installs it, and a build without it will fail loudly at
the first ``.. argparse::`` directive rather than quietly emitting empty pages.
"""

from mageck2.version import __version__

project = "MAGeCK2"
author = "Wei Li lab"
copyright = "2026, Wei Li lab, University of Maryland School of Medicine"

# The reference pages are generated from the installed MAGeCK2, so the version
# shown is by construction the one the options were read from.
version = __version__
release = __version__

extensions = [
    "myst_parser",
    "sphinxarg.ext",
    "sphinx_copybutton",
    "sphinx_design",
]

# Required: pages cross-link to each other's headings with GitHub-style anchors
# (e.g. FILE_FORMATS.md#count-outputs). Without this, MyST generates no heading
# anchors and every one of those links breaks.
myst_heading_anchors = 3

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "attrs_inline",
    # Honours explicit heading ids written as `## Title {#anchor}`. FILE_FORMATS.md
    # uses one so that "Design matrix (`-d` / `--design-matrix`)" can be linked as
    # #design-matrix; without this the attribute is treated as part of the title
    # and the link does not resolve.
    "attrs_block",
]

exclude_patterns = ["_build", "requirements.txt"]

html_theme = "furo"
html_static_path = ["_static"]
html_title = f"MAGeCK2 {version}"

# SourceForge and its project pages answer linkcheck's requests with 403 while
# serving the same URLs normally in a browser. Checking them reports failures
# that say nothing about this repository, so they are skipped rather than
# allowed to drown out a real dead link.
linkcheck_ignore = [
    r"https://sourceforge\.net/.*",
    r"https://bowtie-bio\.sourceforge\.net/.*",
]
linkcheck_timeout = 20

# Nearly every page is a command line or a file format; copy buttons should not
# pick up the shell prompt when one is shown.
copybutton_prompt_text = r"\$ "
copybutton_prompt_is_regexp = True
