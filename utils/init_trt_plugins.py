
def init_trt_plugins():
    # Register TensorRT plugins
    trt.init_libnvinfer_plugins(TRT_LOGGER, "")

