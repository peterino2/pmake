# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
import os
import shutil
from shutil import ignore_patterns
import sys

orig_dir = os.path.abspath(os.path.dirname(__file__))

project = "Embersong"
copyright = "2021, Peter Li"
author = "Peter Li"


def get_git_root(startpath=None):
    root = startpath
    if not startpath:
        root = "."

    levels = 20
    root_found = False

    while not root_found:
        dirs = os.listdir(root)
        if ".git" not in dirs:
            levels -= 1
            assert levels > 0

            root = os.path.join(root, "../")
        else:
            root_found = True
    return os.path.abspath(root)


repo_root = get_git_root()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_inline_tabs",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx.ext.todo",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_logo = "assets/logo.svg"
html_theme_options = {
    "logo_only": True,
}
