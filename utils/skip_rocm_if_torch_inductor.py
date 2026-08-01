
def skipRocmIfTorchInductor(msg="test doesn't currently work with torchinductor on the ROCm stack"):
    return skipIfTorchInductor(msg=msg, condition=TEST_WITH_ROCM and TEST_WITH_TORCHINDUCTOR)

