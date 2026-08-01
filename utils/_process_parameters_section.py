
def _process_parameters_section(
    func_documentation,
    sig,
    func,
    class_name,
    model_name_lowercase,
    parent_class,
    indent_level,
    source_args_dict,
    allowed_params,
):
    """
    Process the parameters section of the docstring.

    Args:
        func_documentation (`str`): Existing function documentation (manually specified in the docstring)
        sig (`inspect.Signature`): Function signature
        func (`function`): Function the parameters belong to
        class_name (`str`): Name of the class the function belongs to
        model_name_lowercase (`str`): Lowercase model name
        parent_class (`class`): Parent class of the function (if any)
        indent_level (`int`): Indentation level
    """
    # Start Args section — constant string, min_indent is always 0, so skip set_min_indent
    docstring = " " * (indent_level + 4) + "Args:\n"
    undocumented_parameters = []
    documented_params = {}
    documented_kwargs = {}

    # Parse existing docstring if available
    if func_documentation is not None:
        documented_params, func_documentation = parse_docstring(func_documentation)

    # Process regular parameters
    param_docstring, missing_args = _process_regular_parameters(
        sig,
        func,
        class_name,
        documented_params,
        indent_level,
        undocumented_parameters,
        source_args_dict,
        parent_class,
        allowed_params,
    )
    docstring += param_docstring

    # Process **kwargs parameters if needed
    kwargs_docstring, kwargs_summary = _process_kwargs_parameters(
        sig, func, parent_class, documented_kwargs, indent_level, undocumented_parameters
    )
    docstring += kwargs_docstring

    # Add return_tensors for processor __call__ methods if not already present
    docstring = _add_return_tensors_to_docstring(func, parent_class, docstring, indent_level)

    # Add **kwargs summary line after return_tensors
    docstring += kwargs_summary

    # Report undocumented parameters
    if len(undocumented_parameters) > 0:
        print("\n".join(undocumented_parameters))

    return docstring

