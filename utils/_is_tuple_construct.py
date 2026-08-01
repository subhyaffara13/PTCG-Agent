
def _is_tuple_construct(x: _C.Value) -> bool:
    return x.node().kind() == "prim::TupleConstruct"

