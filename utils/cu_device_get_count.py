
def cuDeviceGetCount():
    return (CUresult.CUDA_SUCCESS, torch.cuda.device_count())

