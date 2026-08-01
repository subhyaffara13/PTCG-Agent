
def _create_op_prefix(name: str) -> str:
    r"""Takes a native function name converts to an op prefix name.

    Note that the "name" parameter must be the native function name
    without the optional variant suffix, so "add" instead of
    "add.out".

    OP names correspond to classes, hence the change to title case.

    Example::

        >>> _create_op_prefix("add")
        'AddBackward'
    """
    camel_case = "".join([p.title() for p in name.split("_")])
    return (camel_case + "Backward").replace("ForwardBackward", "Backward")

