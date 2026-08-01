
def get_overload_no_implementation_error_message(kind, obj):
    sourcelines, file_lineno, filename = get_source_lines_and_file(obj)
    return (
        f'Implementation for the {kind} "{_qualified_name(obj)}" is missing. Please make '
        f"sure a definition is provided and defined after all overload declarations.\n"
        f'File "{filename}", line {file_lineno}:\n'
        + "".join(sourcelines)
        + "\n"
        + _OVERLOAD_EXAMPLE
    )

