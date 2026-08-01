
def _polyfilled_function_ids() -> set[int]:
    # See also @torch._dynamo.decorators.substitute_in_graph(...), which adds items in _polyfilled_function_ids
    return set()

