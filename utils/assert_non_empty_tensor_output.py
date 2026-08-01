
def assert_non_empty_tensor_output(output: list[Any], api: str) -> None:
    if (len(output) == 1 and output[0] is None) or len(output) < 1:
        raise RuntimeError(
            f"{api}: Expected f to be a function that has non-empty output (got output = {output})"
        )
    for o in output:
        if not isinstance(o, torch.Tensor):
            raise RuntimeError(
                f"{api}: expected f(*primals) to return only tensors"
                f", got unsupported type {type(o)}"
            )

