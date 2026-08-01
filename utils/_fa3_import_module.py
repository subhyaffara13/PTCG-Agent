
def _fa3_import_module(module_path: str) -> None:
    importlib.import_module(module_path)
    if not hasattr(torch.ops, "flash_attn_3"):
        raise RuntimeError(f"Module '{module_path}' does not expose FA3 kernels")
    if not hasattr(torch.ops.flash_attn_3, "fwd"):
        raise RuntimeError(
            f"Module '{module_path}' does not expose FA3 forward kernels"
        )
    if not hasattr(torch.ops.flash_attn_3, "bwd"):
        raise RuntimeError(
            f"Module '{module_path}' does not expose FA3 backward kernels"
        )
    global _FA3_CUDA_FWD, _FA3_CUDA_BWD
    _FA3_CUDA_FWD = torch.ops.flash_attn_3.fwd
    _FA3_CUDA_BWD = torch.ops.flash_attn_3.bwd

