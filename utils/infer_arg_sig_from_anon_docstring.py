
def infer_arg_sig_from_anon_docstring(docstr: str) -> list[ArgSig]:
    """Convert signature in form of "(self: TestClass, arg0: str='ada')" to List[TypedArgList]."""
    ret = infer_sig_from_docstring("stub" + docstr, "stub")
    if ret:
        return ret[0].args
    return []

