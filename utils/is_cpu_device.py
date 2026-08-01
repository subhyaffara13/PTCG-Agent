
def is_cpu_device(inputs: Sequence[torch.Tensor]) -> bool:
    return all(
        item.device == torch.device("cpu")
        for item in inputs
        if isinstance(item, torch.Tensor)
    )

