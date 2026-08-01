
def get_hash(content: str | bytes, extra: str = "", hash_type: str = "code") -> str:
    if hash_type in {"amdgcn", "code", "ptx", "spv"}:
        return code_hash(content, extra)
    if hash_type in {"cubin", "hsaco", XPU_KERNEL_FORMAT}:
        return code_hash(repr(content))
    raise AssertionError(f"Unknown hash type {hash_type}")

