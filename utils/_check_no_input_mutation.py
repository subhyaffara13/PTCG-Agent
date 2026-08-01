
def _check_no_input_mutation(
    flat_args: tuple[Any, ...],
    version_before: list[int],
    mutated_arg_indices: str = "",
) -> None:
    mutated_set = _parse_mutated_arg_indices(mutated_arg_indices)
    for i, arg in enumerate(flat_args):
        if isinstance(arg, torch.Tensor) and arg._version != version_before[i]:
            if i not in mutated_set:
                raise RuntimeError(
                    f"Undeclared in-place mutation on input tensor at position {i}. "
                    f"Declare it in @leaf_function(mutates_args=...) or avoid mutating inputs."
                )

