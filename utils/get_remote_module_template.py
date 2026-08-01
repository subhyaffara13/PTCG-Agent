
def get_remote_module_template(enable_moving_cpu_tensors_to_cuda: bool):
    return _TEMPLATE_PREFIX + (
        _REMOTE_FORWARD_TEMPLATE_ENABLE_MOVING_CPU_TENSORS_TO_CUDA
        if enable_moving_cpu_tensors_to_cuda
        else _REMOTE_FORWARD_TEMPLATE
    )

