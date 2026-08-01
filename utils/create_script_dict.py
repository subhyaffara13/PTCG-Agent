
def create_script_dict(obj):
    """
    Create a ``torch._C.ScriptDict`` instance with the data from ``obj``.

    Args:
        obj (dict): The Python dictionary that is used to initialize the ``ScriptDict``
                    returned by this function.

    Returns:
        An instance of ``torch._C.ScriptDict`` that has the same data as ``obj``
        and can be passed between Python and TorchScript with reference semantics and
        zero copy overhead.
    """
    return torch._C.ScriptDict(obj)  # type: ignore[attr-defined]

