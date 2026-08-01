
def triton_kernel_wrapper_mutation_functionalize(
    ctx: "BaseFunctionalizeAPI",
    kernel_idx: int,
    constant_args_idx: int,
    grid: list["TritonGridType"],
    tma_descriptor_metadata: TMADescriptorMetadata,
    kwargs: dict[str, Any],
) -> None:
    unwrapped_kwargs = ctx.unwrap_tensors(kwargs)  # type: ignore[arg-type]
    # TODO(oulgen): Preexisting bug, if two kernel inputs are views of each
    # other, and one gets mutated in kernel, and later another gets mutated,
    # they are no longer equal. Fix this by graph breaking on this condition
    # earlier in dynamo.
    tensors_to_clone = get_mutated_tensors(
        kernel_idx, constant_args_idx, unwrapped_kwargs, tma_descriptor_metadata
    )
    with ctx.redispatch_to_next():
        unwrapped_outputs = triton_kernel_wrapper_functional(
            kernel_idx=kernel_idx,
            constant_args_idx=constant_args_idx,
            grid=grid,
            tma_descriptor_metadata=tma_descriptor_metadata,
            kwargs=unwrapped_kwargs,
            tensors_to_clone=tensors_to_clone,
        )

    if not set(unwrapped_outputs.keys()).issubset(set(kwargs.keys())):
        raise AssertionError(
            f"Output keys {set(unwrapped_outputs.keys())} not subset of input keys {set(kwargs.keys())}"
        )
    for key, output_arg in unwrapped_outputs.items():
        if not isinstance(output_arg, Tensor):
            continue
        input_arg = kwargs[key]
        if not isinstance(input_arg, Tensor):
            raise AssertionError(
                f"Expected input_arg for key {key} to be a Tensor, got {type(input_arg)}"
            )

        ctx.replace(input_arg, output_arg)
        # indicate that above replace is hidden from autograd
        ctx.mark_mutation_hidden_from_autograd(input_arg)
        ctx.commit_update(input_arg)
        ctx.sync(input_arg)
    return None

