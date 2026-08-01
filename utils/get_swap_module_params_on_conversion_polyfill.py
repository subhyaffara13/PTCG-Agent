
def get_swap_module_params_on_conversion_polyfill() -> bool:
    """
    Polyfill for torch.__future__.get_swap_module_params_on_conversion.

    Returns the actual value from the underlying global variable.
    """
    # Access the module's global variable directly to avoid recursion
    import torch.__future__ as torch_future

    return torch_future._swap_module_params_on_conversion

