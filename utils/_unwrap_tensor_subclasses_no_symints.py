
def _unwrap_tensor_subclasses_no_symints(
    args: list[Any],
) -> list[Any]:
    return runtime_unwrap_tensor_subclasses(args, append_symints=False)  # type: ignore[arg-type]

