
def _process_returns_section(func_documentation, sig, config_class, indent_level):
    """
    Process the returns section of the docstring.

    Args:
        func_documentation (`str`): Existing function documentation (manually specified in the docstring)
        sig (`inspect.Signature`): Function signature
        config_class (`str`): Config class for the model
        indent_level (`int`): Indentation level
    """
    return_docstring = ""

    # Extract returns section from existing docstring if available
    if func_documentation is not None and (match_start := _re_return.search(func_documentation)) is not None:
        match_end = _re_example.search(func_documentation)
        if match_end:
            return_docstring = func_documentation[match_start.start() : match_end.start()]
            func_documentation = func_documentation[match_end.start() :]
        else:
            return_docstring = func_documentation[match_start.start() :]
            func_documentation = ""
        return_docstring = set_min_indent(return_docstring, indent_level + 4)
    # Otherwise, generate return docstring from return annotation if available
    elif sig.return_annotation is not None and sig.return_annotation != inspect._empty:
        add_intro, return_annotation = contains_type(sig.return_annotation, ModelOutput)
        return_docstring = _prepare_return_docstring(return_annotation, config_class, add_intro=add_intro)
        # PT_RETURN_INTRODUCTION already starts with \n, so only add blank line if it doesn't start with one
        if not return_docstring.startswith("\n"):
            return_docstring = "\n" + return_docstring
        return_docstring = set_min_indent(return_docstring, indent_level + 4)

    return return_docstring, func_documentation

