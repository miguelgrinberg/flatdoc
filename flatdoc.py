"""
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

    \"\"\"# Foo

    This module does foo.

    !INCLUDE Bar, func
    \"\"\"
    class Bar:
        \"\"\"## Bar

        This class does bar.

        !INCLUDE baz
        \"\"\"
        def baz(self):
            \"\"\"### baz()

            This method does baz.
            \"\"\"
            pass

    def func():
        \"\"\"## func()

        This function does func.
        \"\"\"
        pass
    \"\"\"

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

!INCLUDE main

API Reference
-------------

!INCLUDE flatdoc
"""
from importlib import import_module
from inspect import cleandoc
import sys
from types import ModuleType

from qualname import qualname

__all__ = ['flatdoc']


def fullname(obj):
    """Return a fully qualified name for a module, function, class, etc."""
    if hasattr(obj, '__module__'):
        return obj.__module__ + '.' + qualname(obj)
    else:
        return obj.__name__


def is_module(mod):
    return isinstance(mod, ModuleType)


def get_docs(objs):
    """Generate documentation for a module, function, class or method."""
    obj = objs[0]
    if obj.__doc__ is None:
        raise ValueError('No docstring available for ' + fullname(obj))

    # process each line of the docstring and resolve includes
    doc = ''
    for line in cleandoc(obj.__doc__).splitlines():
        line = line.rstrip()
        if not line.startswith('!INCLUDE '):
            # this is a normal line, add it to the output text
            doc += line + '\n'
        else:
            # this is an include directive
            subobjs = objs[:]
            for inc in [x.strip() for x in line[9:].split(',')]:
                subobj = subobjs[0]
                # ensure we can resolve this include
                if line.endswith('.'):
                    raise ValueError(
                        '{}: include cannot end in a period'.format(
                            fullname(subobj)))

                # find the object referenced by the include
                for subname in inc.split('.'):
                    if subname == '':
                        del subobjs[0]
                        if len(subobjs) == 0:
                            raise ValueError('Include {} is reaching above '
                                             'start module'.format(inc))
                    elif getattr(subobj, subname, None) is None:
                        # if a submodule is specified, we need to import it
                        if subobj is not None and not is_module(subobj):
                            raise ValueError('{} does not exist'.format(
                                subobj.__name__ + '.' + subname))
                        name = subobj.__name__ + '.' + subname
                        subobjs.insert(0, import_module(name))
                    else:
                        # if a function, class or method is specified, just
                        # retrieve it
                        subobjs.insert(0, getattr(subobj, subname))
                    subobj = subobjs[0] if len(subobjs) > 0 else None
                # generate the docs for the included object
                doc += get_docs(subobjs)
                while not doc.endswith('\n\n'):
                    doc += '\n'
    return doc


def flatdoc(name):
    """
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
    """
    mod = import_module(name)
    return get_docs([mod])


def main():
    """
    Command Line Usage
    ------------------

    The ``flatdoc`` utility can be used to generate documentation from the
    command line. The only argument this command takes is the import name of
    the top-level object to generate documentation for.

    This documentation you are reading was generated with the following
    command::

        flatdoc flatdoc > README.rst
    """
    print(flatdoc(sys.argv[1]))  # pragma: no cover
