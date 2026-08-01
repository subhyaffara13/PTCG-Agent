
def test_api_per_method(
    index_or_series,
    dtype,
    any_allowed_skipna_inferred_dtype,
    any_string_method,
    request,
    using_infer_string,
):
    # this test does not check correctness of the different methods,
    # just that the methods work on the specified (inferred) dtypes,
    # and raise on all others
    box = index_or_series

    # one instance of each parametrized fixture
    inferred_dtype, values = any_allowed_skipna_inferred_dtype
    method_name, args, kwargs = any_string_method

    reason = None
    if box is Index and values.size == 0:
        if method_name in ["partition", "rpartition"] and kwargs.get("expand", True):
            raises = TypeError
            reason = "Method cannot deal with empty Index"
        elif method_name == "split" and kwargs.get("expand", None):
            raises = TypeError
            reason = "Split fails on empty Series when expand=True"
        elif method_name == "get_dummies":
            raises = ValueError
            reason = "Need to fortify get_dummies corner cases"

    elif (
        box is Index
        and inferred_dtype == "empty"
        and dtype == object
        and method_name == "get_dummies"
    ):
        raises = ValueError
        reason = "Need to fortify get_dummies corner cases"

    if reason is not None:
        mark = pytest.mark.xfail(raises=raises, reason=reason)
        request.applymarker(mark)

    t = box(values, dtype=dtype)  # explicit dtype to avoid casting
    method = getattr(t.str, method_name)

    if using_infer_string and dtype == "category":
        string_allowed = method_name not in ["decode"]
    else:
        string_allowed = True
    bytes_allowed = method_name in ["decode", "get", "len", "slice"]
    # as of v0.23.4, all methods except 'cat' are very lenient with the
    # allowed data types, just returning NaN for entries that error.
    # This could be changed with an 'errors'-kwarg to the `str`-accessor,
    # see discussion in GH 13877
    mixed_allowed = method_name not in ["cat"]

    allowed_types = (
        ["empty"]
        + ["string", "unicode"] * string_allowed
        + ["bytes"] * bytes_allowed
        + ["mixed", "mixed-integer"] * mixed_allowed
    )

    if inferred_dtype in allowed_types:
        # xref GH 23555, GH 23556
        method(*args, **kwargs)  # works!
    else:
        # GH 23011, GH 23163
        msg = (
            f"Cannot use .str.{method_name} with values of "
            f"inferred dtype {inferred_dtype!r}."
            "|a bytes-like object is required, not 'str'"
        )
        with pytest.raises(TypeError, match=msg):
            method(*args, **kwargs)

