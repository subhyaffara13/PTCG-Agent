
def evaluate_platform_supports_mxfp8_grouped_gemm():
    if torch.cuda.is_available() and not torch.version.hip:
        built_with_mslk = "USE_MSLK" in torch.__config__.show()
        return built_with_mslk and IS_SM100
    return False

