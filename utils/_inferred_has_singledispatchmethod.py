
def _inferred_has_singledispatchmethod(target: nodes.NodeNG) -> bool:
    """
    Infer `target` and return True if the inferred object has a
    @singledispatchmethod decorator.
    """
    inferred = utils.safe_infer(target)
    if not inferred:
        return False

    if isinstance(inferred, (nodes.FunctionDef, nodes.AsyncFunctionDef)):
        decorators = inferred.decorators
        if isinstance(decorators, nodes.Decorators):
            for dec in decorators.nodes:
                inferred_dec = utils.safe_infer(dec)
                if (
                    inferred_dec
                    and inferred_dec.qname() == "functools.singledispatchmethod"
                ):
                    return True

    return False

