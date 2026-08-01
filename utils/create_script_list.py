
def create_script_list(obj, type_hint=None):
    """
    Create a ``torch._C.ScriptList`` instance with the data from ``obj``.

    Args:
        obj (dict): The Python list that is used to initialize the ``ScriptList``
                    returned by this function.
    Returns:
        An instance of ``torch._C.ScriptList`` that has the same data as ``obj``
        and can be passed between Python and TorchScript with reference semantics and
        zero copy overhead.
    """
    return torch._C.ScriptList(obj)  # type: ignore[attr-defined]

