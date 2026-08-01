
def _suppresses_exception(
    call: nodes.Call, exception: type[Exception] | str = Exception
) -> bool:
    """Check if the given node suppresses the given exception."""
    if not isinstance(exception, str):
        exception = exception.__name__
    for arg in call.args:
        match inferred := safe_infer(arg):
            case nodes.ClassDef():
                if inferred.name == exception:
                    return True
            case nodes.Tuple():
                for elt in inferred.elts:
                    inferred_elt = safe_infer(elt)
                    if (
                        isinstance(inferred_elt, nodes.ClassDef)
                        and inferred_elt.name == exception
                    ):
                        return True
    return False

