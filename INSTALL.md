# Installation

## Prerequisites

mageck2 requires:

* Python &ge; 3.7
* A C++ compiler and `make`, used to build the bundled RRA component. The build uses the
  system `c++` driver (`g++` on Linux, `clang++` on macOS); you can override it with
  `make CC=...` if needed.
* R / RStudio (optional; only if you want to generate HTML reports from the R Markdown files)

The Python package dependencies (numpy, scipy, pandas, matplotlib, statsmodels) are installed
automatically by pip.

## Installation from GitHub

The recommended way to install mageck2 is with `pip`.

Install the latest version directly:

    pip install git+https://github.com/davidliwei/mageck2.git

or clone the repository and install from a local copy:

    git clone https://github.com/davidliwei/mageck2.git
    cd mageck2
    pip install .

To install into your user environment without root privileges, add `--user`:

    pip install --user git+https://github.com/davidliwei/mageck2.git

## Test the installation

In your command line, type

    mageck2

to see if it works. You should see the list of available subcommands.

## Troubleshooting: "command not found"

`pip` installs the `mageck2` and `RRA` programs into the environment's `bin` directory. If you
see a "command not found" error after a `--user` installation, that directory may not be on your
`PATH`. Find where pip installed the scripts:

    python -m site --user-base

and add its `bin` subdirectory to your `PATH`. For example, if the base is `/Users/john/.local`:

    export PATH=$PATH:/Users/john/.local/bin
