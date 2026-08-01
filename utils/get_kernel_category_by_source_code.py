
def get_kernel_category_by_source_code(src_code: str) -> str:
    """
    Similar to get_kernel_category but use the source code. Call this API
    if we have not compile the src_code to module yet.
    """
    choices = [
        ch for ch in _kernel_category_choices if f"@triton_heuristics.{ch}" in src_code
    ]
    if len(choices) == 1:
        return choices[0]
    else:
        return "unknown"

