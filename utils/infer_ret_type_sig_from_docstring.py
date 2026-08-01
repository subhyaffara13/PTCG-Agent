
def infer_ret_type_sig_from_docstring(docstr: str, name: str) -> str | None:
    """Convert signature in form of "func(self: TestClass, arg0) -> int" to their return type."""
    ret = infer_sig_from_docstring(docstr, name)
    if ret:
        return ret[0].ret_type
    return None

