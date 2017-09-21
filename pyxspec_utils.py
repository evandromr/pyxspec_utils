# coding: utf-8
""" Useful python functions to use with Pyxspec"""


def showmodel(m):
    """Print current model information

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
    """
    print("Model: {}".format(m.expression))
    print()
    print("{:4} {:4} {:12} {:10} {:7} {:15} {:12}".format("P#",
                                                          "C#",
                                                          "Component",
                                                          "Parameter",
                                                          "Unit",
                                                          "Value",
                                                          "Errors"))
    print("--"*38)
    pid = 1
    for cid, component in enumerate(m.componentNames):
        for parameter in eval("m.{}.parameterNames".format(component)):
            u = eval("m.{}.{}.unit".format(component, parameter))
            val = eval("m.{}.{}.values[0]".format(component, parameter))
            err = eval("m.{}.{}.error[:2]".format(component, parameter))
            print("{:<4} {:<4} {:<12} {:<10} {:<7} {:<10.5} \
                   ({:<10.5}, {:<10.5})".format(pid, cid + 1, component,
                                                parameter, u, val,
                                                err[0], err[1]))
            pid += 1
