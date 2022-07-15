.. paleos documentation master file, created by
   sphinx-quickstart on Sat Mar 26 09:38:02 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to paleos's documentation!
==================================

The paleos package is a simple entry point for those requiring common data 
wrangling used in paleoclimate or paleoceanography research. It relies on the
standard python scientific computing stack including numpy, scipy, pandas etc.

Most of the existing functionality in paleos focuses on age model manipulation 
and application. More features may be added over time depending on what is
useful. For other more advanced use cases, users are suggested to refer to 
`pyleoclim <https://pypi.org/project/pyleoclim/>`_.

To get the quickest overview of paleos, please see the examples. The full API
reference gives more details about the individual functions.

.. toctree::
   :maxdepth: 3
   :caption: User Guide:

   examples/index.rst

.. toctree::
   :maxdepth: 3
   :caption: API reference:

   paleos.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
