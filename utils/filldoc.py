
def filldoc(docdict: Mapping[str, str], unindent_params: bool = True) -> Decorator:
    """Return docstring decorator using docdict variable dictionary.

    Parameters
    ----------
    docdict : dict[str, str]
        A dictionary containing name, docstring fragment pairs.
    unindent_params : bool, optional
        If True, strip common indentation from all parameters in docdict.
        Default is False.

    Returns
    -------
    decfunc : function
        The decorator function that applies dictionary to its
        argument's __doc__ attribute.
    """
    if unindent_params:
        docdict = unindent_dict(docdict)

    def decorate(func: _F) -> _F:
        # __doc__ may be None for optimized Python (-OO)
        doc = func.__doc__ or ""
        func.__doc__ = docformat(doc, docdict)
        return func

    return decorate

