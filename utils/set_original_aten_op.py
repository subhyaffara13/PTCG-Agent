
def set_original_aten_op(
    func: OpOverload | torch._ops.HigherOrderOperator,
) -> Generator[None, None, None]:
    if ORIGINAL_ATEN.get() is None and fx_traceback.has_preserved_node_meta():
        token = ORIGINAL_ATEN.set(func)
        fx_traceback.current_meta["original_aten"] = func
        try:
            yield
        finally:
            ORIGINAL_ATEN.reset(token)
            fx_traceback.current_meta["original_aten"] = None
    else:
        yield

