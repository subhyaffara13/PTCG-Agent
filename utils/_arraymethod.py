
def _arraymethod(funcname, onmask=True):
    """
    Return a class method wrapper around a basic array method.

    Creates a class method which returns a masked array, where the new
    ``_data`` array is the output of the corresponding basic method called
    on the original ``_data``.

    If `onmask` is True, the new mask is the output of the method called
    on the initial mask. Otherwise, the new mask is just a reference
    to the initial mask.

    Parameters
    ----------
    funcname : str
        Name of the function to apply on data.
    onmask : bool
        Whether the mask must be processed also (True) or left
        alone (False). Default is True. Make available as `_onmask`
        attribute.

    Returns
    -------
    method : instancemethod
        Class method wrapper of the specified basic array method.

    """
    def wrapped_method(self, *args, **params):
        result = getattr(self._data, funcname)(*args, **params)
        result = result.view(type(self))
        result._update_from(self)
        mask = self._mask
        if not onmask:
            result.__setmask__(mask)
        elif mask is not nomask:
            # __setmask__ makes a copy, which we don't want
            result._mask = getattr(mask, funcname)(*args, **params)
        return result
    methdoc = getattr(ndarray, funcname, None) or getattr(np, funcname, None)
    if methdoc is not None:
        wrapped_method.__doc__ = methdoc.__doc__
    wrapped_method.__name__ = funcname
    return wrapped_method

