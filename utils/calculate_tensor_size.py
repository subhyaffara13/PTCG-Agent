
def calculate_tensor_size(tensor: torch.Tensor) -> float:
    """
    Calculate the size of a PyTorch tensor in megabytes (MB).

    Args:
        tensor (torch.Tensor): Input tensor

    Returns:
        float: Memory size in MB
    """
    # Get number of elements and size per element
    num_elements = tensor.numel()
    element_size = tensor.element_size()

    return (num_elements * element_size) / (1024 * 1024)

