
def cudaGetDeviceProperties(d):
    class DummyError:
        value = False

    return (DummyError(), torch.cuda.get_device_properties(d))

