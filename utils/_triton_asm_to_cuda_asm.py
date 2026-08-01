
def _triton_asm_to_cuda_asm(asm_str: str) -> str:
    return _TRITON_ARG_RE.sub(r"%\1", asm_str)

