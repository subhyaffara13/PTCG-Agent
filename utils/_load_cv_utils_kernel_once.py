
def _load_cv_utils_kernel_once():
    """Load cv_utils_kernel once on first use."""
    global cv_utils_kernel
    if cv_utils_kernel is not None:
        return  # Already attempted loading (successfully or not)

    if not is_kernels_available():
        logger.warning_once(
            "kernels library is not installed. NMS post-processing, hole filling, and sprinkle removal will be skipped. "
            "Install it with `pip install kernels` for better mask quality."
        )
        cv_utils_kernel = False
        return

    try:
        cv_utils_kernel = get_kernel("kernels-community/cv-utils")
    except Exception as e:
        logger.warning_once(
            f"Failed to load cv_utils kernel (your torch/cuda setup may not be supported): {e}. "
            "NMS post-processing, hole filling, and sprinkle removal will be skipped."
        )
        cv_utils_kernel = False

