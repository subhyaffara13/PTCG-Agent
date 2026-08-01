
def _is_invalid_isinstance_type(arg: nodes.NodeNG) -> bool:
    # Return True if we are sure that arg is not a type
    if isinstance(arg, nodes.BinOp) and arg.op == "|":
        return any(
            _is_invalid_isinstance_type(elt) and not is_none(elt)
            for elt in (arg.left, arg.right)
        )
    match inferred := utils.safe_infer(arg):
        case _ if not inferred:
            # Cannot infer it so skip it.
            return False
        case nodes.Tuple():
            return any(_is_invalid_isinstance_type(elt) for elt in inferred.elts)
        case nodes.ClassDef():
            return False
        case astroid.Instance() if inferred.qname() == BUILTIN_TUPLE:
            return False
        case bases.UnionType():
            return any(
                _is_invalid_isinstance_type(elt) and not is_none(elt)
                for elt in (inferred.left, inferred.right)
            )
    return True

