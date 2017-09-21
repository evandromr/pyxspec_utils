# PyXspec Utils
**Author:** Evandro M. Ribeiro

---
Tools that makes my life easier when using PyXspec on a Jupyter notebook.

## Contents

 - pyxspec_utils.py
    A module with help functions to make some repetitive pyxspec commands easier
    to use

 - array2xspec.py
    Functions to read a txt file or python array and transform into a pha file
    readable to pyXspec

## Dependencies


 - PyXspec
 - Astropy
 - Numpy

[Xspec](https://heasarc.gsfc.nasa.gov/xanadu/xspec/) is an X-Ray spectral fitting package and [PyXspec]() is it's python implementation.  
[Jupyter notebooks](http://jupyter.org/index.html) is an interactive way to use Python.  
And [Python](https://www.python.org/) is a programming language.

## Documentation and Usage

Some examples are shown at the [Examples](examples.md) files

Doc-strings are available for each function inside the module.


Import as a python module:

```python
    import pyxspec_utils
```
To show all available functions run:

```python
    help(pyxspec_utils)
```

Individual help for each function can be accessed with:

```python
    help(pyxspec_utils.<function>)
```
Where `<function>` us one of the available functions

On Jupyter or Ipython you cal also access the help with

```python
    pyxspec_utils.function?
```
