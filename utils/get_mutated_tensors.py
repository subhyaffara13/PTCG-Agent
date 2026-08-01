
def get_mutated_tensors(
    kernel_idx: int,
    constant_args_idx: int,
    kwargs: dict[str, Any],
    tma_descriptor_metadata: TMADescriptorMetadata,
) -> list[str]:
    kernel = kernel_side_table.get_kernel(kernel_idx)
    constant_args = kernel_side_table.get_constant_args(constant_args_idx)
    tensor_accesses = identify_accessed_tensors(
        kernel, {**kwargs, **constant_args}, tma_descriptor_metadata
    )
    # Filter to only tensor kwargs: with Triton 3.7+, ordered_arg_names
    # includes scalars, so writes may reference non-tensor args like SymInts.
    return [
        dep.name
        for dep in tensor_accesses.read_writes.writes
        if isinstance(kwargs.get(dep.name), Tensor)
    ]

