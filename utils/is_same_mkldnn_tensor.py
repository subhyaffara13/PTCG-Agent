
def is_same_mkldnn_tensor(data: torch.Tensor, value: torch.Tensor) -> bool:
    return (
        data.is_mkldnn
        and data.size() == value.size()
        and data.dtype == value.dtype
        and data.device == value.device
        and torch.ops.mkldnn.data_ptr(data) == torch.ops.mkldnn.data_ptr(value)
    )

