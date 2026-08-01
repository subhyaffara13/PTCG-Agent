
def _list_unsupported_tensor_ops():
    header = """\n\n
Unsupported Tensor Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    methods, properties = _gen_unsupported_methods_properties()
    return (
        header
        + "\n"
        + methods
        + """

Unsupported Tensor Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
        + "\n"
        + properties
    )

