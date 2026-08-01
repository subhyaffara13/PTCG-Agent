
def _get_elts(arg, context):
    def is_iterable(n) -> bool:
        return isinstance(n, (nodes.List, nodes.Tuple, nodes.Set))

    try:
        inferred = next(arg.infer(context))
    except (InferenceError, StopIteration) as exc:
        raise UseInferenceDefault from exc
    if isinstance(inferred, nodes.Dict):
        items = inferred.items
    elif is_iterable(inferred):
        items = []
        for elt in inferred.elts:
            # If an item is not a pair of two items,
            # then fallback to the default inference.
            # Also, take in consideration only hashable items,
            # tuples and consts. We are choosing Names as well.
            if not is_iterable(elt):
                raise UseInferenceDefault()
            if len(elt.elts) != 2:
                raise UseInferenceDefault()
            if not isinstance(elt.elts[0], (nodes.Tuple, nodes.Const, nodes.Name)):
                raise UseInferenceDefault()
            items.append(tuple(elt.elts))
    else:
        raise UseInferenceDefault()
    return items

