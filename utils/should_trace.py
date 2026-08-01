
def should_trace(f: NativeFunction) -> bool:
    # Operations involving Storage or Type are not traceable at the moment
    if any(
        str(arg.type) in {"Storage", "Type"} for arg in f.func.schema_order_arguments()
    ):
        return False
    # We can't trace functions which don't have any Tensor or TensorList returns
    if not any(r.type.is_tensor_like() for r in f.func.returns):
        return False
    return f.func.name.name.base not in DONT_RECORD_TRACE

