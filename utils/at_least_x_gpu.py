
def at_least_x_gpu(x):
    if TEST_CUDA and torch.cuda.device_count() >= x:
        return True
    if TEST_HPU and torch.hpu.device_count() >= x:
        return True
    if TEST_XPU and torch.xpu.device_count() >= x:
        return True
    return False

