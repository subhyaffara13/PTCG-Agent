
def auto_method_docstring(
    func,
    parent_class=None,
    custom_intro=None,
    custom_args=None,
    checkpoint=None,
    source_args_dict=None,
    allowed_params=None,
):
    """
    Wrapper that automatically generates docstring.
    """

    # Use inspect to retrieve the method's signature
    sig = inspect.signature(func)
    indent_level = get_indent_level(func) if not parent_class else get_indent_level(parent_class)

    # Get model information
    model_name_lowercase, class_name, config_class = _get_model_info(func, parent_class)
    func_documentation = func.__doc__

    if custom_args is not None and func_documentation is not None:
        func_documentation = "\n" + set_min_indent(custom_args.strip("\n"), 0) + "\n" + func_documentation
    elif custom_args is not None:
        func_documentation = "\n" + set_min_indent(custom_args.strip("\n"), 0)

    # Add intro to the docstring before args description if needed
    if custom_intro is not None:
        docstring = set_min_indent(custom_intro, indent_level + 4)
        if not docstring.strip().endswith("\n"):
            docstring += "\n"
    else:
        docstring = add_intro_docstring(func, class_name=class_name, indent_level=indent_level)

    # Process Parameters section
    docstring += _process_parameters_section(
        func_documentation,
        sig,
        func,
        class_name,
        model_name_lowercase,
        parent_class,
        indent_level,
        source_args_dict,
        allowed_params,
    )

    # Process Returns section
    return_docstring, func_documentation = _process_returns_section(
        func_documentation, sig, config_class, indent_level
    )
    docstring += return_docstring

    # Process Example section
    example_docstring = _process_example_section(
        func_documentation,
        func,
        parent_class,
        class_name,
        model_name_lowercase,
        config_class,
        checkpoint,
        indent_level,
    )
    docstring += example_docstring

    # Format the docstring with the placeholders
    docstring = format_args_docstring(docstring, model_name_lowercase)

    # Assign the dynamically generated docstring to the wrapper function
    func.__doc__ = docstring
    return func

