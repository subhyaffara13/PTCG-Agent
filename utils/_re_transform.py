
def _re_transform() -> nodes.Module:
    return parse(
        """
    from collections import namedtuple
    _Method = namedtuple('_Method', 'name ident salt_chars total_size')

    METHOD_SHA512 = _Method('SHA512', '6', 16, 106)
    METHOD_SHA256 = _Method('SHA256', '5', 16, 63)
    METHOD_BLOWFISH = _Method('BLOWFISH', 2, 'b', 22)
    METHOD_MD5 = _Method('MD5', '1', 8, 34)
    METHOD_CRYPT = _Method('CRYPT', None, 2, 13)
    """
    )


def _re_transform() -> nodes.Module:
    # The RegexFlag enum exposes all its entries by updating globals()
    # In 3.6-3.10 all flags come from sre_compile
    # On 3.11+ all flags come from re._compiler
    if PY311_PLUS:
        import_compiler = "import re._compiler as _compiler"
    else:
        import_compiler = "import sre_compile as _compiler"
    return parse(
        f"""
    {import_compiler}
    NOFLAG = 0
    ASCII = _compiler.SRE_FLAG_ASCII
    IGNORECASE = _compiler.SRE_FLAG_IGNORECASE
    LOCALE = _compiler.SRE_FLAG_LOCALE
    UNICODE = _compiler.SRE_FLAG_UNICODE
    MULTILINE = _compiler.SRE_FLAG_MULTILINE
    DOTALL = _compiler.SRE_FLAG_DOTALL
    VERBOSE = _compiler.SRE_FLAG_VERBOSE
    TEMPLATE = _compiler.SRE_FLAG_TEMPLATE
    DEBUG = _compiler.SRE_FLAG_DEBUG
    A = ASCII
    I = IGNORECASE
    L = LOCALE
    U = UNICODE
    M = MULTILINE
    S = DOTALL
    X = VERBOSE
    T = TEMPLATE
    """
    )

