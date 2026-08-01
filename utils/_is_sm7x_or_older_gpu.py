
def _is_sm7x_or_older_gpu(index: int | None) -> bool:
    props = torch.cuda.get_device_properties(index or 0)
    return props.major <= 7

