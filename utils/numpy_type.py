
def numpy_type(torch_type):
    type_map = {
        torch.float32: np.float32,
        torch.float16: np.float16,
        torch.int32: np.int32,
        torch.int64: np.longlong,
    }
    return type_map[torch_type]

