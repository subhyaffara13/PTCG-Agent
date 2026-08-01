
def infer_typing_namedtuple_function(node, context: InferenceContext | None = None):
    """
    Starting with python3.9, NamedTuple is a function of the typing module.
    The class NamedTuple is build dynamically through a call to `type` during
    initialization of the `_NamedTuple` variable.
    """
    klass = extract_node(
        """
        from typing import _NamedTuple
        _NamedTuple
        """
    )
    return klass.infer(context)

