
def _parse_proper_kernel_fn_code(kernel_fn_code: str) -> str:
    """
    Skip decorators.
    """
    start_pos = kernel_fn_code.index("def ")
    return kernel_fn_code[start_pos:]

