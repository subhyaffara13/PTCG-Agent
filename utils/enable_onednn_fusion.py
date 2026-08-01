
def enable_onednn_fusion(enabled: bool) -> None:
    """Enable or disables onednn JIT fusion based on the parameter `enabled`.

    .. deprecated:: 2.5
        TorchScript is deprecated, please use ``torch.compile`` instead.
    """
    torch._C._jit_set_llga_enabled(enabled)

