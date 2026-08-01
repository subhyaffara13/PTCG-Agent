
def _unwrap_no_symints(args: list[Any]) -> list[Any]:
    return runtime_unwrap_tensor_subclasses(args, append_symints=False)

