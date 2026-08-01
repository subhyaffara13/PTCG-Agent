
def evaluate_platform_supports_fp8_grouped_gemm():
    if torch.cuda.is_available():
        if torch.version.hip:
            if "USE_MSLK" not in torch.__config__.show():
                return False
            archs = ['gfx942', 'gfx950']
            for arch in archs:
                if arch in torch.cuda.get_device_properties(0).gcnArchName:
                    return True
        else:
            return SM90OrLater and not SM100OrLater
    return False

