
def compile_llvm_ir_to_code_object(
    llvm_ir_path: str, output_path: str, target_arch: str
) -> bool:
    """
    Compile unbundled LLVM IR to a single-arch code object.

    Args:
        llvm_ir_path: Path to .ll file
        output_path: Where to write .hsaco file
        target_arch: Target architecture (e.g., 'gfx90a')

    Returns:
        True if successful
    """
    if not os.path.exists(llvm_ir_path):
        return False

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        clang = get_rocm_compiler()
    except RuntimeError:
        return False

    # Sanitize LLVM IR to remove attributes unsupported by ROCm's clang
    llvm_ir_path = _sanitize_llvm_ir_for_rocm(llvm_ir_path)

    # Using clang and not hipcc since we are not compiling source code
    # Instead we use the LLVM IR (.ll) provided by triton
    cmd = [
        clang,
        "-target",
        "amdgcn-amd-amdhsa",
        f"-mcpu={target_arch}",
        llvm_ir_path,
        "-o",
        output_path,
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)

        if not os.path.exists(output_path):
            return False

        return True

    except subprocess.CalledProcessError:
        return False

