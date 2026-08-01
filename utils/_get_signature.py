
def _get_signature(fn: Any) -> inspect.Signature:
    return inspect.signature(fn, follow_wrapped=False)

