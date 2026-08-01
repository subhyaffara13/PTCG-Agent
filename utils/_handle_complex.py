
def _handle_complex(tensor):
    """
    Returns a real view of a tensor if complex dtype else just the tensor
    need to check if a UninitializedParameter because otherwise checking is_complex is an error for a LazyModule
    """
    return (
        torch.view_as_real(tensor)
        if not isinstance(tensor, torch.nn.UninitializedParameter)
        and tensor.is_complex()
        else tensor
    )

