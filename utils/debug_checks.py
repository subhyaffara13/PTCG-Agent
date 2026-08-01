
def debug_checks(code: types.CodeType) -> None:
    """Make sure our assembler produces same bytes as we start with"""
    dode, _ = transform_code_object(code, lambda x, y: None, safe=True)
    assert code.co_code == dode.co_code, debug_bytes(code.co_code, dode.co_code)

