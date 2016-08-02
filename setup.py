from setuptools import setup, find_packages

version = '0.1'

setup(name='pysh',
      version=version,
      description="Smart wrapper to write shell commands as python code",
      long_description="""\
This module translates python function calls with args and kwargs to POSIX command line execution. Positional parameters
are translated to positional command line arguments. Named parameters are translated to flags (one character keyword
argument will be treated as short flag, multi character keyword argument will be treated as long flag).
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Tomasz Iwanek',
      author_email='',
      url='https://github.com/tiwanek/pysh',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
