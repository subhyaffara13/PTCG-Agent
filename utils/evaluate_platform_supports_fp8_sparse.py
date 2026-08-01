
def evaluate_platform_supports_fp8_sparse():
    if torch.cuda.is_available():
        if torch.version.hip:
            return 'gfx950' in torch.cuda.get_device_properties(0).gcnArchName
        else:
            return (
                (SM90OrLater or torch.cuda.get_device_capability() == (8, 9))
                and torch.backends.cusparselt.is_available()
                and torch.backends.cusparselt.version() >= 602
            )
    return False

