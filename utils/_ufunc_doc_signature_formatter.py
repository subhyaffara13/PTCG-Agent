
def _ufunc_doc_signature_formatter(ufunc):
    """
    Builds a signature string which resembles PEP 457

    This is used to construct the first line of the docstring

    Keep in sync with `_ufunc_inspect_signature_builder`.
    """

    # input arguments are simple
    if ufunc.nin == 1:
        in_args = 'x'
    else:
        in_args = ', '.join(f'x{i + 1}' for i in range(ufunc.nin))

    # output arguments are both keyword or positional
    if ufunc.nout == 0:
        out_args = ', /, out=()'
    elif ufunc.nout == 1:
        out_args = ', /, out=None'
    else:
        out_args = '[, {positional}], / [, out={default}]'.format(
            positional=', '.join(
                f'out{i + 1}' for i in range(ufunc.nout)),
            default=repr((None,) * ufunc.nout)
        )

    # keyword only args depend on whether this is a gufunc
    kwargs = (
        ", casting='same_kind'"
        ", order='K'"
        ", dtype=None"
        ", subok=True"
    )

    # NOTE: gufuncs may or may not support the `axis` parameter
    if ufunc.signature is None:
        kwargs = f", where=True{kwargs}[, signature]"
    else:
        kwargs += "[, signature, axes, axis]"

    # join all the parts together
    return f'{ufunc.__name__}({in_args}{out_args}, *{kwargs})'

