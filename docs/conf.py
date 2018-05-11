#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# serpentTools documentation build configuration file, created by
# sphinx-quickstart on Tue Oct 10 20:03:11 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from unittest.mock import MagicMock

ON_RTD = os.environ.get('READTHEDOCS', None) == 'True'

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'serpentTools'
copyright = (
    u'2017-2018, <a href='
    '"https://github.com/CORE-GATECH-GROUP/serpent-tools/blob/develop/'
    'README.rst#contributors">The serpentTools developer team</a>'
    ', GTRC')
author = 'The serpentTools developer team'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

version = '0.4.0'
release = '0.4.0'
# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# external link shortcuts for sphinx.ext.extlinks
extlinks = {
    'issue': ('https://github.com/CORE-GATECH-GROUP/serpent-tools/'
              'issues/%s', '#'),
    'pull': ('https://github.com/CORE-GATECH-GROUP/serpent-tools/'
             'pull/%s', '#'), 
    'release-tag': ('https://github.com/CORE-GATECH-GROUP/serpent-tools/'
                    'releases/tag/%s', '')
}
# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'github_user': 'CORE-GATECH-GROUP',
    'github_repo': 'serpent-tools',
    'sidebar_width': '260px',
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'searchbox.html'
    ]
}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'serpentToolsdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'serpentTools.tex', 'serpentTools Documentation',
     author, 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'serpentTools', 'serpentTools Documentation',
     [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'serpentTools', 'serpentTools Documentation',
     author, 'serpentTools', 'Parsings tools for the SERPENT Monte Carlo Code',
     'Miscellaneous'),
]

# -- Options for auto documentation --------------------------------------
autodoc_default_flags = ['members', 'show-inheritance']

# -- Links to external documentation
intersphinx_mapping = {
        'python': ('https://docs.python.org/3.5', None),
        'matplotlib': ('https://matplotlib.org', None),
        'numpy': ('https://docs.scipy.org/doc/numpy/', None)
    }

