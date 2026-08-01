
def evaluate_platform_supports_ck_sdpa():
    if TEST_WITH_ROCM:
        return torch.backends.cuda.is_ck_sdpa_available()
    else:
        return False

