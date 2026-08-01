
def _ufunc_inspect_signature_builder(ufunc):
    """
    Builds a ``__signature__`` string.

    Should be kept in sync with `_ufunc_doc_signature_formatter`.
    """

    from inspect import Parameter, Signature

    params = []

    # positional-only input parameters
    if ufunc.nin == 1:
        params.append(Parameter("x", Parameter.POSITIONAL_ONLY))
    else:
        params.extend(
            Parameter(f"x{i}", Parameter.POSITIONAL_ONLY)
            for i in range(1, ufunc.nin + 1)
        )

    # for the sake of simplicity, we only consider a single output parameter
    if ufunc.nout == 1:
        out_default = None
    else:
        out_default = (None,) * ufunc.nout
    params.append(
        Parameter("out", Parameter.POSITIONAL_OR_KEYWORD, default=out_default),
    )

    if ufunc.signature is None:
        params.append(Parameter("where", Parameter.KEYWORD_ONLY, default=True))
    else:
        # NOTE: not all gufuncs support the `axis` parameters
        params.append(Parameter("axes", Parameter.KEYWORD_ONLY, default=_NoValue))
        params.append(Parameter("axis", Parameter.KEYWORD_ONLY, default=_NoValue))
        params.append(Parameter("keepdims", Parameter.KEYWORD_ONLY, default=False))

    params.extend((
        Parameter("casting", Parameter.KEYWORD_ONLY, default='same_kind'),
        Parameter("order", Parameter.KEYWORD_ONLY, default='K'),
        Parameter("dtype", Parameter.KEYWORD_ONLY, default=None),
        Parameter("subok", Parameter.KEYWORD_ONLY, default=True),
        Parameter("signature", Parameter.KEYWORD_ONLY, default=None),
    ))

    return Signature(params)

