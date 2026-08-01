
def evaluate_platform_supports_bf16():
    if torch.version.cuda:
        return SM80OrLater
    elif torch.version.hip:
        return True
    elif TEST_XPU:
        return True
    return False

