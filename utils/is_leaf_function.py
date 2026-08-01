
def is_leaf_function(obj: Any) -> bool:
    _maybe_init_lazy_module(obj)
    return id(obj) in _leaf_function_ids

