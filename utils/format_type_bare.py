
def format_type_bare(
    typ: Type, options: Options, verbosity: int = 0, module_names: bool = False
) -> str:
    """
    Convert a type to a relatively short string suitable for error messages.

    `verbosity` is a coarse-grained control on the verbosity of the type
    `fullnames` specifies a set of names that should be printed in full

    This function will return an unquoted string.  If a caller doesn't need to
    perform post-processing on the string output, format_type should be used
    instead.  (The caller may want to use quote_type_string after
    processing has happened, to maintain consistent quoting in messages.)
    """
    return format_type_inner(typ, verbosity, options, find_type_overlaps(typ), module_names)

