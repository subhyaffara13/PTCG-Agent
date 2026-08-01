
def _add_data_doc(docstring, replace_names):
    """
    Add documentation for a *data* field to the given docstring.

    Parameters
    ----------
    docstring : str
        The input docstring.
    replace_names : list of str or None
        The list of parameter names which arguments should be replaced by
        ``data[name]`` (if ``data[name]`` does not throw an exception).  If
        None, replacement is attempted for all arguments.

    Returns
    -------
    str
        The augmented docstring.
    """
    if (docstring is None
            or replace_names is not None and len(replace_names) == 0):
        return docstring
    docstring = inspect.cleandoc(docstring)

    data_doc = ("""\
    If given, all parameters also accept a string ``s``, which is
    interpreted as ``data[s]`` if ``s`` is a key in ``data``."""
                if replace_names is None else f"""\
    If given, the following parameters also accept a string ``s``, which is
    interpreted as ``data[s]`` if ``s`` is a key in ``data``:

    {', '.join(map('*{}*'.format, replace_names))}""")
    # using string replacement instead of formatting has the advantages
    # 1) simpler indent handling
    # 2) prevent problems with formatting characters '{', '%' in the docstring
    if _log.level <= logging.DEBUG:
        # test_data_parameter_replacement() tests against these log messages
        # make sure to keep message and test in sync
        if "data : indexable object, optional" not in docstring:
            _log.debug("data parameter docstring error: no data parameter")
        if 'DATA_PARAMETER_PLACEHOLDER' not in docstring:
            _log.debug("data parameter docstring error: missing placeholder")
    return docstring.replace('    DATA_PARAMETER_PLACEHOLDER', data_doc)

