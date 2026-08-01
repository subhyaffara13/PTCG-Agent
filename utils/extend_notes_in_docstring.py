
def extend_notes_in_docstring(cls: object, notes: str) -> Decorator:
    """This decorator replaces the decorated function's docstring
    with the docstring from corresponding method in `cls`.
    It extends the 'Notes' section of that docstring to include
    the given `notes`.

    Parameters
    ----------
    cls : type or object
        A class with a method with the same name as the decorated method.
        The docstring of the method in this class replaces the docstring of the
        decorated method.
    notes : str
        Additional notes to append to the 'Notes' section of the docstring.

    Returns
    -------
    decfunc : function
        The decorator function that modifies the __doc__ attribute
        of its argument.
    """

    def _doc(func: _F) -> _F:
        cls_docstring = getattr(cls, func.__name__).__doc__
        # If python is called with -OO option,
        # there is no docstring
        if cls_docstring is None:
            return func
        end_of_notes = cls_docstring.find("        References\n")
        if end_of_notes == -1:
            end_of_notes = cls_docstring.find("        Examples\n")
            if end_of_notes == -1:
                end_of_notes = len(cls_docstring)
        func.__doc__ = (
            cls_docstring[:end_of_notes] + notes + cls_docstring[end_of_notes:]
        )
        return func

    return _doc

