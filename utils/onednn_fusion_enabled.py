
def onednn_fusion_enabled():
    """Return whether onednn JIT fusion is enabled.

    .. deprecated:: 2.5
        TorchScript is deprecated, please use ``torch.compile`` instead.
    """
    return torch._C._jit_llga_enabled()

