
def is_expression(value: str) -> bool:
    """Validate SPDX license expression.

    .. note::
        Utilizes `license-expression library`_ to
        validate SPDX compound expression according to `SPDX license expression spec`_.

    .. _SPDX license expression spec: https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/
    .. _license-expression library: https://github.com/nexB/license-expression
    """
    try:
        res = __SPDX_EXPRESSION_LICENSING.validate(value)
    except Exception:
        # the throw happens when internals crash due to unexpected input characters.
        return False
    return 0 == len(res.errors)

