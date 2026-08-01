
def evaluate_platform_supports_mx_gemm():
    if torch.cuda.is_available():
        if torch.version.hip:
            if ROCM_VERSION >= (7, 0):
                return 'gfx950' in torch.cuda.get_device_properties(0).gcnArchName
        else:
            return SM100OrLater
    return False

