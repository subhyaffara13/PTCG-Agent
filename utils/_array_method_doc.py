
def _array_method_doc(name: str, params: str, doc: str) -> None:
    """
    Interenal helper function for adding docstrings to a common method of
    `numpy.ndarray` and `numpy.generic`.

    The provided docstring will be added to the given `numpy.ndarray` method.
    For the  `numpy.generic` method, a shorter docstring indicating that it is
    identical to the `ndarray` method will be created.
    Both methods will have a proper and identical `__text_signature__`.

    Parameters
    ----------
    name : str
        Name of the method.
    params : str
        Parameter signature for the method without parentheses, for example,
        ``"a, /, dtype=None, *, copy=False"``.
        Parameter defaults must be understood by `ast.literal_eval`, i.e. strings,
        bytes, numbers, tuples, lists, dicts, sets, booleans, or None.
    doc : str
        The full docstring for the `ndarray` method.
    """

    # prepend the pos-only `$self` parameter to the method signature
    if "/" not in params:
        params = f"/, {params}" if params else "/"
    params = f"$self, {params}"

    # add docstring to `np.ndarray.{name}`
    doc = textwrap.dedent(doc).strip()
    doc_array = _METHOD_DOC_TEMPLATE.format(name=name, params=params, doc=doc)
    add_newdoc("numpy._core.multiarray", "ndarray", (name, doc_array))

    # add docstring to `np.generic.{name}`
    doc_scalar = f"Scalar method identical to `ndarray.{name}`."
    doc_scalar = _METHOD_DOC_TEMPLATE.format(name=name, params=params, doc=doc_scalar)
    add_newdoc("numpy._core.numerictypes", "generic", (name, doc_scalar))

