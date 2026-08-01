
def _validate_mllama_preprocess_arguments(do_resize, size, do_pad, max_image_tiles):
    if not do_pad:
        raise ValueError("MllamaImageProcessor doesn't support `do_pad=False` mode.")
    if not do_resize:
        raise ValueError("MllamaImageProcessor doesn't support `do_resize=False` mode.")
    if max_image_tiles is None or max_image_tiles <= 0:
        raise ValueError(f"MllamaImageProcessor `max_image_tiles` must be a positive integer, got {max_image_tiles}.")
    _validate_size(size)


def _validate_mllama_preprocess_arguments(do_resize, size, do_pad, max_image_tiles):
    if not do_pad:
        raise ValueError("MllamaImageProcessor doesn't support `do_pad=False` mode.")
    if not do_resize:
        raise ValueError("MllamaImageProcessor doesn't support `do_resize=False` mode.")
    if max_image_tiles is None or max_image_tiles <= 0:
        raise ValueError(f"MllamaImageProcessor `max_image_tiles` must be a positive integer, got {max_image_tiles}.")
    _validate_size(size)

