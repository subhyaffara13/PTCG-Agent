
def get_ort_device_type(device_type: str) -> int:
    if device_type == "cuda":
        return C.OrtDevice.cuda()
    elif device_type == "cann":
        return C.OrtDevice.cann()
    elif device_type == "cpu":
        return C.OrtDevice.cpu()
    elif device_type == "dml":
        return C.OrtDevice.dml()
    elif device_type == "webgpu":
        return C.OrtDevice.webgpu()
    elif device_type == "gpu":
        return C.OrtDevice.gpu()
    elif device_type == "npu":
        return C.OrtDevice.npu()
    else:
        raise Exception("Unsupported device type: " + device_type)

