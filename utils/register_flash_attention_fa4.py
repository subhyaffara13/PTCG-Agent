
def register_flash_attention_fa4(
    module_path: str = "flash_attn.cute.interface",
) -> _FA4Handle:
    """
    Register FA4 flash attention kernels with the PyTorch dispatcher.

    Args:
        module_path: Python module path to the FA4 implementation.
    """
    global _FA4_MODULE_PATH
    _ = _fa4_import_module(module_path)
    _FA4_MODULE_PATH = module_path
    return _FA4Handle(_fa4_register_kernels())

