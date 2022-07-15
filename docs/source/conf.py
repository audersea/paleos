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
import os
import re
import paleos
from sphinx_gallery.sorting import FileNameSortKey
import plotly.io as pio
from plotly.io._sg_scraper import plotly_sg_scraper

# for sphinx gallery
pio.renderers.default = "sphinx_gallery_png"

# -- Project information -----------------------------------------------------

project = "paleos"
copyright = "2022, Neeraj Shah, Alexandra Auderset"
author = "Neeraj Shah, Alexandra Auderset"

# version information
release = paleos.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "matplotlib.sphinxext.plot_directive",
    "sphinx_gallery.gen_gallery",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["setup.rst", "modules.rst"]

# autodoc configuration
autosectionlabel_prefix_document = True
autodoc_member_order = "bysource"
autodoc_undoc_members = False

# intersphinx
intersphinx_mapping = {
    "numpy": ("https://numpy.org/doc/stable/", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
}

# sphinx gallery
image_scrapers = ("matplotlib", plotly_sg_scraper)
sphinx_gallery_conf = {
    "run_stale_examples": False,
    "filename_pattern": f"{re.escape(os.sep)}eg_",
    "remove_config_comments": True,
    "thumbnail_size": (300, 300),
    "examples_dirs": "../../examples/",
    "gallery_dirs": "examples",
    "image_scrapers": image_scrapers,
    "within_subsection_order": FileNameSortKey,
}

# code styles
pygments_style = "sphinx"
pygments_dark_style = "monokai"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"
html_theme_options = {
    "navigation_with_keys": True,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# some custom css
def setup(app):
    app.add_css_file("custom_gallery.css")
