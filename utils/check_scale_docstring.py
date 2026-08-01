
def check_scale_docstring(distfn):
    if distfn.__doc__ is not None:
        # Docstrings can be stripped if interpreter is run with -OO
        npt.assert_('scale' not in distfn.__doc__)

