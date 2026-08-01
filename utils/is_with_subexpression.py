
def is_with_subexpression(tokens_tripple):
    """
    Return True if a ``tokens_tripple`` Token tripple is a "WITH" license sub-
    expression.
    """
    lic, wit, exc = tokens_tripple
    return (
        isinstance(lic.value, LicenseSymbol)
        and wit.value == KW_WITH
        and isinstance(exc.value, LicenseSymbol)
    )

