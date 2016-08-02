PySh
====

Introduction
------------

Bored with writing tedious wrappers around bash commands?

Here is smart wrapper that will directly translate your python code into POSIX command line execution.

This module translates python function calls with args and kwargs to POSIX command line execution. Positional parameters
are translated to positional command line arguments. Named parameters are translated to flags (one character keyword
argument will be treated as short flag, multi-character keyword argument will be treated as long flag).

Keyworded arguments accepts:
 - bool - to indicate if boolean flag is present or not
 - string - to indicate value of flag
 - list of string - to indicate repetition of given flag with multiple values

Usage
-----

Below are examples showing usage.

Running simple command
~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    echo -n "Print no new line"

.. code:: python

    pysh.echo(n=True, "Print no new line")

Running command with short and long flags
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    myprogram -o value_of_short_option --ooo value_of_long_option

.. code:: python

    pysh.myprogram(o="value_of_short_option", ooo="value_of_long_option")

Running command with subcommands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    git commit -a --amend -m "My new titile"

.. code:: python

    pysh.git.commit(a=True, m="My new title", amend=True)

Escaping hyphen mark
~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    git ls-files

.. code:: python

    pysh.git.ls__files()

Running with single flag specified multiple times
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    myprogram -a file1 -a file2 -a file3

.. code:: python

    pysh.myprogram(a=["file1", "file2", "file3"])

Checking status of execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    pysh_result = pysh.myprogram()
    print(pysh_result.exit_code)

Branching upon command result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    if pysh.stat("myfile"):
        pysh.rm("myfile")

Reading command output
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    pysh_result = pysh.myprogram()
    print(pysh_result.output.read())

Raw arguments
~~~~~~~~~~~~~

.. code:: bash

    java -jar my.jar

.. code:: python

    pysh.java("-jar", "my.jar")

Configuring pysh object
=======================

PySh object may be configured to behave differently than default one.

Instead of using default pysh object:

.. code:: python

    from pysh import pysh

user code can created on configured PySh object:

.. code:: python

    from pysh import PySh
    mysh = Pysh()
    mysh[pysh.THROW_AT_ERROR] = True # throw PyShException when command fails (returns non-zero exit code)
    mysh[pysh.IGNORE_OUTPUT] = True # do not catch output of command


:Authors:
    Tomasz Iwanek