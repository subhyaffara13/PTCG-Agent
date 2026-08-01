
def get_kernel_category(kernel_mod: ModuleType) -> str:
    """
    Given the module defining a triton kernel, return the category of the kernel.
    Category can be one of:
    - pointwise
    - reduction
    - persistent_reduction

    Currently we simply decide the category depending on what decorator is imported
    by the kernel.
    """
    choices = [ch for ch in _kernel_category_choices if ch in kernel_mod.__dict__]
    if len(choices) == 1:
        return choices[0]
    else:
        return "unknown"

