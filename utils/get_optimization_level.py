
def get_optimization_level(level):
    """Convert string to GraphOptimizationLevel."""
    if level == "disable":
        return ort.GraphOptimizationLevel.ORT_DISABLE_ALL
    if level == "basic":
        # Constant folding and other optimizations that only use ONNX operators
        return ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
    if level == "extended":
        # Optimizations using custom operators, excluding NCHWc and NHWC layout optimizers
        return ort.GraphOptimizationLevel.ORT_ENABLE_EXTENDED
    if level == "layout":
        # NCHWc and NHWC layout optimizers
        return ort.GraphOptimizationLevel.ORT_ENABLE_LAYOUT
    if level == "all":
        return ort.GraphOptimizationLevel.ORT_ENABLE_ALL

    raise ValueError("Invalid optimization level of " + level)

