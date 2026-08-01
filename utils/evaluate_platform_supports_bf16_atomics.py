
def evaluate_platform_supports_bf16_atomics():
    if torch.version.cuda:
        return SM80OrLater
    elif torch.version.hip:
        return ROCM_VERSION >= (8, 0)
    return False

