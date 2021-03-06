.. START Source defined in docs/github_docs.py


.. This document was procedurally generated by docs/github_docs.py on Saturday, January 23, 2016


.. END Source defined in docs/github_docs.py
.. START Source defined in docs/github_docs.py


.. role:: mod(literal)
.. role:: func(literal)
.. role:: data(literal)
.. role:: const(literal)
.. role:: class(literal)
.. role:: meth(literal)
.. role:: attr(literal)
.. role:: exc(literal)
.. role:: obj(literal)
.. role:: envvar(literal)


.. END Source defined in docs/github_docs.py
.. START Source defined in docs/source/_partial/readme_title.rst

========
pureyaml
========

.. image:: https://badge.fury.io/py/pureyaml.svg
    :target: https://pypi.python.org/pypi/pureyaml/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/pureyaml.svg
    :target: https://pypi.python.org/pypi/pureyaml/
    :alt: Development Status

.. image:: https://travis-ci.org/bionikspoon/pureyaml.svg?branch=develop
    :target: https://travis-ci.org/bionikspoon/pureyaml?branch=develop
    :alt: Build Status

.. image:: https://coveralls.io/repos/bionikspoon/pureyaml/badge.svg?branch=develop
    :target: https://coveralls.io/github/bionikspoon/pureyaml?branch=develop&service=github
    :alt: Coverage Status

.. image:: https://readthedocs.org/projects/pureyaml/badge/?version=develop
    :target: https://pureyaml.readthedocs.org/en/develop/?badge=develop
    :alt: Documentation Status


Yet another yaml parser, in pure python.


.. END Source defined in docs/source/_partial/readme_title.rst
.. START Source defined in docs/source/_partial/readme_features.rst

Features
--------

- Documentation: https://pureyaml.readthedocs.org
- Open Source: https://github.com/bionikspoon/pureyaml
- MIT license


- YAML encoder/decoder written in pure python


.. END Source defined in docs/source/_partial/readme_features.rst
.. START Source defined in docs/source/installation.rst


============
Installation
============

At the command line either via easy_install or pip

.. code-block:: shell

    $ pip install pureyaml



.. code-block:: shell

    $ easy_install pureyaml

Or, if you have virtualenvwrapper installed

.. code-block:: shell

    $ mkvirtualenv pureyaml
    $ pip install pureyaml

**Uninstall**

.. code-block:: shell

    $ pip uninstall pureyaml


.. END Source defined in docs/source/installation.rst
.. START Source defined in docs/source/usage.rst


=====
Usage
=====

To use pureyaml in a project

.. code-block:: python

    import pureyaml

    >>> import pureyaml
    >>> from textwrap import dedent
    >>> from pprint import pprint
    >>> text = dedent("""
    ...     marvel:
    ...     - iron man
    ...     - the hulk
    ...     - captain america
    ...     dc:
    ...     - batman
    ...     - the joker
    ...     - superman
    ... """)[1:]

    >>> pprint(pureyaml.load(text))
    {'dc': ['batman', 'the joker', 'superman'],
     'marvel': ['iron man', 'the hulk', 'captain america']}

    >>> print(pureyaml.dump(pureyaml.load(text)))
    dc:
    - batman
    - the joker
    - superman
    marvel:
    - iron man
    - the hulk
    - captain america


.. END Source defined in docs/source/usage.rst
.. START Source defined in docs/source/_partial/readme_credits.rst

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `bionikspoon/cookiecutter-pypackage`_ forked from `audreyr/cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`bionikspoon/cookiecutter-pypackage`: https://github.com/bionikspoon/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


.. END Source defined in docs/source/_partial/readme_credits.rst
