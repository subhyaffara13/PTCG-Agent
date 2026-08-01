
def _parse_kernel_line_of_code(proper_kernel_fn_code: str) -> int:
    """
    Return the line of code for the kernel excluding the decorators.
    """
    return len(proper_kernel_fn_code.splitlines())

