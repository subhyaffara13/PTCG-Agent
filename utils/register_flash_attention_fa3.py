
def register_flash_attention_fa3(
    module_path: str = "flash_attn_interface",
) -> _FA3Handle:
    """
    Register FA3 flash attention kernels with the PyTorch dispatcher.

    Args:
        module_path: Python module path to the FA3 implementation.
    """
    _fa3_import_module(module_path)

    # Expose FA3 registration status to C++
    torch._C._set_sdp_use_fa3(True)

    return _FA3Handle(_fa3_register_kernels())

