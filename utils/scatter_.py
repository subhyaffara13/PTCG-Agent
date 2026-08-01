
def scatter_(self, dim: int, index, src, *, reduce: str | None = None):
    assert reduce in (None, "add", "multiply")
    if reduce is None:
        op_overload = getattr(aten.scatter_, V.graph.current_node.target._overloadname)  # type: ignore[union-attr]
        fallback_result = scatter_fallback(
            op_overload, self, dim, index, src, reduce=reduce
        )
        if fallback_result is not None:
            return fallback_result

    if reduce == "add":
        reduce = "sum"
    elif reduce == "multiply":
        reduce = "prod"
    return scatter_reduce_(self, dim, index, src, reduce)

