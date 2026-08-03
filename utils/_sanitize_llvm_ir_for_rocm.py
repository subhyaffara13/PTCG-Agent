import re

def _sanitize_llvm_ir_for_rocm(llvm_ir_path: str) -> str:
    """
    Sanitize LLVM IR to be compatible with ROCm's clang.

    Triton's LLVM (upstream) may emit attributes and metadata that ROCm's
    older clang does not yet support. Only strips attributes confirmed to
    cause parse errors — preserves all others to maintain correct codegen.

    Currently strips:
        - nocreateundeforpoison: function attribute (upstream LLVM, not in ROCm)
        - dwarfAddressSpace: debug metadata field (upstream LLVM, not in ROCm)

    Returns:
        Path to sanitized .ll file, or original path if no changes needed.
    """
    with open(llvm_ir_path) as f:
        content = f.read()

    sanitized = content
    sanitized = re.sub(r"\bnocreateundeforpoison\b\s*", "", sanitized)
    sanitized = re.sub(r",\s*dwarfAddressSpace:\s*\d+", "", sanitized)

    if sanitized == content:
        return llvm_ir_path

    sanitized_path = llvm_ir_path + ".sanitized.ll"
    with open(sanitized_path, "w") as f:
        f.write(sanitized)

    log.debug(
        "Sanitized LLVM IR for ROCm clang compatibility: %s -> %s",
        llvm_ir_path,
        sanitized_path,
    )
    return sanitized_path

