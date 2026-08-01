
def measure_gpu_memory(monitor_type, func, start_memory=None):
    return measure_memory(is_gpu=True, func=func, monitor_type=monitor_type, start_memory=start_memory)

