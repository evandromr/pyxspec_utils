
# Examples of function in `pyxspec_utils`

## Initial setup


```python
# Import xspec and pyxspec_utils
import xspec
import pyxspec_utils
```


```python
# Define a model
m = xspec.Model("wabs(powerlaw+mekal)")
```

## `showmodel()`


```python
pyxspec_utils.showmodel(m)
```

    Model: wabs(powerlaw + mekal)

    P#   C#   Component    Parameter  Unit    Value           Errors      
    ----------------------------------------------------------------------------
    1    1    wabs         nH         10^22   1.0                       (0.0000e+00, 0.0000e+00)
    2    2    powerlaw     PhoIndex           1.0                       (0.0000e+00, 0.0000e+00)
    3    2    powerlaw     norm               1.0                       (0.0000e+00, 0.0000e+00)
    4    3    mekal        kT         keV     1.0                       (0.0000e+00, 0.0000e+00)
    5    3    mekal        nH         cm-3    1.0                       (0.0000e+00, 0.0000e+00)
    6    3    mekal        Abundanc           1.0                       (0.0000e+00, 0.0000e+00)
    7    3    mekal        Redshift           0.0                       (0.0000e+00, 0.0000e+00)
    8    3    mekal        switch             1.0                       (0.0000e+00, 0.0000e+00)
    9    3    mekal        norm               1.0                       (0.0000e+00, 0.0000e+00)



```python
# Show help message
help(pyxspec_utils.showmodel)
```

    Help on function showmodel in module pyxspec_utils:

    showmodel(m)
        Print current model information

        Display a formated view of current model information
        such as the one produced by `model.show()` on pyXspec
        or by `show par` on Xspec.
        The errors are taken from the `xspec.Fit.error` calculation
        if that was not performed errros will be zero.

        Parameters
        ----------
        m: Xspec.Model
            The model from which you want information

        Returns
        --------
        Print output as a formated table

        Example
        --------
        >>> import xspec
        >>> import pyxspec_utils as pu
        >>> m1 = xspec.Models("wabs(powerlaw+mekal)")
        >>> pu.printmodel(m1)
        Model: wabs(powerlaw + mekal)
        P#   C#   Component    Parameter  Unit    Value        Errors
        -------------------------------------------------------------
        1    1    wabs         nH         10^22   1.0     (0.0 , 0.0)
        2    2    powerlaw     PhoIndex           1.0     (0.0 , 0.0)
        3    2    powerlaw     norm               1.0     (0.0 , 0.0)
        4    3    mekal        kT         keV     1.0     (0.0 , 0.0)
        5    3    mekal        nH         cm-3    1.0     (0.0 , 0.0)
        6    3    mekal        Abundanc           1.0     (0.0 , 0.0)
        7    3    mekal        Redshift           0.0     (0.0 , 0.0)
        8    3    mekal        switch             1.0     (0.0 , 0.0)
        9    3    mekal        norm               1.0     (0.0 , 0.0)
