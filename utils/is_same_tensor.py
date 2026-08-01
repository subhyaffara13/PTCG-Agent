
def is_same_tensor(data: torch.Tensor, value: torch.Tensor) -> bool:
    return (
        not data.is_mkldnn
        and data.size() == value.size()
        and data.stride() == value.stride()
        and data.dtype == value.dtype
        and data.device == value.device
        and data.untyped_storage().data_ptr() == value.untyped_storage().data_ptr()
        and data.storage_offset() == value.storage_offset()
    )

