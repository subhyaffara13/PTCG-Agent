
def is_flash_attention_available() -> bool:
    r"""Check if PyTorch was built with FlashAttention for scaled_dot_product_attention.

    Returns:
        True if FlashAttention is built and available; otherwise, False.

    Note:
        This function is dependent on a CUDA-enabled build of PyTorch. It will return False
        in non-CUDA environments.
    """
    return torch._C._is_flash_attention_available()

