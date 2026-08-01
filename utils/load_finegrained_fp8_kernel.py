
def load_finegrained_fp8_kernel() -> FineGrainedFP8:
    if is_torchdynamo_compiling():
        _populate_finegrained_fp8_kernel()
    return _load_finegrained_fp8_kernel()

