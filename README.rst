flatdoc
=======

.. image:: https://travis-ci.org/miguelgrinberg/flatdoc.svg?branch=master
    :target: https://travis-ci.org/miguelgrinberg/flatdoc

flatdoc is a simple tool that generates flat documentation from docstrings that
are defined in modules, functions, classes and methods in your code.

Installation
------------

You can install flatdoc with ``pip``::

    pip install flatdoc

Writing Documentation
---------------------

You can write your module, function, class and method documentation in any
format that you like. Markdown and reStructuredText are both good formats to
use, since they are easy to type, they are very readable, and have the tooling
necessary to generate HTML, PDF, Postscript, etc.

The key to build the flat documentation from all these docstrings is to link
them with the ``!INCLUDE`` directive. As an example, consider the following
module foo.py, with Markdown docstrings::

    """# Foo

    This module does foo.

    !INCLUDE Bar, func
    """
    class Bar:
        """## Bar

        This class does bar.

        !INCLUDE baz
        """
        def baz(self):
            """### baz()

            This method does baz.
            """
            pass

    def func():
        """## func()

        This function does func.
        """
        pass
    """

The generated documentation for the above module would be a consolidated
Markdown file::

    # Foo

    This module does foo.

    ## Bar

    This class does bar.

    ### baz()

    This method does baz.

    ## func()

    This function does func.

The !INCLUDE directive
----------------------

As you've seen in the example in the previous section, documentation lines that
begin with ``!INCLUDE`` are treated as references to other docstrings. With
this mechanism multiple docstrings can be consolidated into a single output
document.

The argument given to ``!INCLUDE`` is a comma-separated list of references to
other docstrings. These references are always relative to the current
docstring, so for example, in a module docstring, any top-level functions or
classes can be referenced by their names, and in a class, all its methods can
also be referenced directly by their names.

When there is a need to reference a docstring that is not a direct subordinate,
a standard dot notation can be used. Using the example of the previous section,
consider the following cases:

- Include method ``baz`` of class ``Bar`` from module ``foo``::

    !INCLUDE Bar.baz

- Include class ``Bar`` from function ``func``::

    !INCLUDE .Bar

- Include a module ``mod`` that exists at the same level as ``foo`` from method
  ``baz``::

    !INCLUDE ...mod

Command Line Usage
------------------

The ``flatdoc`` utility can be used to generate documentation from the
command line. The only argument this command takes is the import name of
the top-level object to generate documentation for.

This documentation you are reading was generated with the following
command::

    flatdoc flatdoc > README.rst


API Reference
-------------

`flatdoc(name)`
~~~~~~~~~~~~~~~

Generates documentation from docstrings.

Parameters
^^^^^^^^^^

======== ======== ===============
  Name     Type     Description
======== ======== ===============
 `name`   string   The import name for the top-level object to document.
======== ======== ===============

Return value
^^^^^^^^^^^^

A string with the flattened documentation.

Example
^^^^^^^

The following example generates the documentation for a package named
``my_pkg`` and prints it to the console::

    from flatdoc import flatdoc
    print(flatdoc('my_pkg'))


