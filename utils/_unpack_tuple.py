
def _unpack_tuple(tuple_value: _C.Value) -> tuple[_C.Value, ...]:
    tuple_node = tuple_value.node()
    if not _is_tuple_construct(tuple_value):
        raise errors.SymbolicValueError(
            f"ONNX symbolic expected node type 'prim::TupleConstruct', "
            f"got '{tuple_node.kind()}'.",
            tuple_value,
        )
    return tuple(tuple_node.inputs())


def _unpack_tuple(x):
    """ Unpacks one-element tuples for use as return values """
    if len(x) == 1:
        return x[0]
    else:
        return x


def _unpack_tuple(tup):
    if len(tup) == 1:
        return tup[0]
    else:
        return tup

