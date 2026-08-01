
def evaluate_platform_supports_half_atomics():
    if torch.version.hip:
        return ROCM_VERSION >= (8, 0)
    return True

