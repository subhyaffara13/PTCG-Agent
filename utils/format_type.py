
def format_type(
    typ: Type, options: Options, verbosity: int = 0, module_names: bool = False
) -> str:
    """
    Convert a type to a relatively short string suitable for error messages.

    `verbosity` is a coarse-grained control on the verbosity of the type

    This function returns a string appropriate for unmodified use in error
    messages; this means that it will be quoted in most cases.  If
    modification of the formatted string is required, callers should use
    format_type_bare.
    """
    return quote_type_string(format_type_bare(typ, options, verbosity, module_names))

