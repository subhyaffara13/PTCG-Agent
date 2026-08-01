
def get_local_tensor_mode_list() -> list["LocalTensorMode"]:
    global _PROCESS_MODE
    if _PROCESS_MODE:
        global _PROCESS_LOCAL_TENSOR_MODE
        return _PROCESS_LOCAL_TENSOR_MODE
    global _THREAD_LOCAL_TENSOR_MODE
    if not hasattr(_THREAD_LOCAL_TENSOR_MODE, "value"):
        _THREAD_LOCAL_TENSOR_MODE.value = []
    return _THREAD_LOCAL_TENSOR_MODE.value

