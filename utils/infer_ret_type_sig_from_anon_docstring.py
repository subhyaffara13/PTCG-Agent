
def infer_ret_type_sig_from_anon_docstring(docstr: str) -> str | None:
    """Convert signature in form of "(self: TestClass, arg0) -> int" to their return type."""
    lines = ["stub" + line.strip() for line in docstr.splitlines() if line.strip().startswith("(")]
    return infer_ret_type_sig_from_docstring("".join(lines), "stub")

