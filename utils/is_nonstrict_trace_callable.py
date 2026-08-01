
def is_nonstrict_trace_callable(obj: Any) -> bool:
    _maybe_init_lazy_module(obj)
    return id(obj) in _nonstrict_trace_callable_ids

