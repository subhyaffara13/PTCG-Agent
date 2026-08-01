
def contains_sys_version_info(expr: Expression) -> None | int | tuple[int | None, int | None]:
    if is_sys_attr(expr, "version_info"):
        return (None, None)  # Same as sys.version_info[:]
    if isinstance(expr, IndexExpr) and is_sys_attr(expr.base, "version_info"):
        index = expr.index
        if isinstance(index, IntExpr):
            return index.value
        if isinstance(index, SliceExpr):
            if index.stride is not None:
                if not isinstance(index.stride, IntExpr) or index.stride.value != 1:
                    return None
            begin = end = None
            if index.begin_index is not None:
                if not isinstance(index.begin_index, IntExpr):
                    return None
                begin = index.begin_index.value
            if index.end_index is not None:
                if not isinstance(index.end_index, IntExpr):
                    return None
                end = index.end_index.value
            return (begin, end)
    return None

