
def load_deepgemm_kernel(requires_sm100: bool = False) -> DeepGEMM:
    if is_torchdynamo_compiling():
        _populate_deepgemm_kernel(requires_sm100=requires_sm100)
    return _load_deepgemm_kernel(requires_sm100=requires_sm100)

