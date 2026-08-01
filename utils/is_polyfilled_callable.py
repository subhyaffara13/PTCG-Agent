
def is_polyfilled_callable(obj: Any) -> bool:
    # See also @torch._dynamo.decorators.substitute_in_graph(...), which adds items in _polyfilled_function_ids
    return id(obj) in _polyfilled_function_ids

