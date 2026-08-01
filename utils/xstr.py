
def xstr(*args):
    sympy_deprecation_warning(
        """
        The sympy.printing.pretty.pretty_symbology.xstr() function is
        deprecated. Use str() instead.
        """,
        deprecated_since_version="1.7",
        active_deprecations_target="deprecated-pretty-printing-functions"
    )
    return str(*args)

