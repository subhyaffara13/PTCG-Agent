
def unpack_infer(stmt, context: InferenceContext | None = None):
    """recursively generate nodes inferred by the given statement.
    If the inferred value is a list or a tuple, recurse on the elements
    """
    if isinstance(stmt, (List, Tuple)):
        for elt in stmt.elts:
            if elt is util.Uninferable:
                yield elt
                continue
            yield from unpack_infer(elt, context)
        return {"node": stmt, "context": context}
    # if inferred is a final node, return it and stop
    inferred = next(stmt.infer(context), util.Uninferable)
    if inferred is stmt:
        yield inferred
        return {"node": stmt, "context": context}
    # else, infer recursively, except Uninferable object that should be returned as is
    for inferred in stmt.infer(context):
        if isinstance(inferred, util.UninferableBase):
            yield inferred
        else:
            yield from unpack_infer(inferred, context)

    return {"node": stmt, "context": context}

