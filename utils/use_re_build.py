
def use_re_build() -> bool:
    """
    Use for CUTLASS compilation only right now.
    """
    if config.is_fbcode() and not cuda_env.nvcc_exist(_cuda_compiler()):
        from triton.fb.re_build_helper import should_build_locally

        return not should_build_locally()
    return False

