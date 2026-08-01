
def assert_non_empty_list_of_tensors(
    output: list[torch.Tensor], api: str, argname: str
) -> None:
    if len(output) == 0:
        raise RuntimeError(f"{api}: Expected {argname} to contain at least one Tensor.")
    for out in output:
        if isinstance(out, torch.Tensor):
            continue
        raise RuntimeError(
            f"{api}: Expected {argname} to only contain Tensors, got {type(out)}"
        )

