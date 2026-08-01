
def evaluate_platform_supports_cudnn_attention():
    return (not TEST_WITH_ROCM) and SM80OrLater and (TEST_CUDNN_VERSION >= 90000)

