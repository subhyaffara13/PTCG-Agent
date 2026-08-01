
def _all_to_all_single(
    input: torch.Tensor,
    output_split_sizes: list[int] | None,
    input_split_sizes: list[int] | None,
    tag: str,
    ranks: list[int],
    group_size: int,
):
    if output_split_sizes is None or input_split_sizes is None:
        if not (output_split_sizes is None and input_split_sizes is None):
            raise AssertionError(
                "output_split_sizes and input_split_sizes must either be "
                "specified together or both set to None"
            )
        output_split_sizes = [input.shape[0] // group_size] * group_size
        input_split_sizes = output_split_sizes

    group_name = c10d._resolve_group_name_by_ranks_and_tag(ranks, tag)
    return torch.ops._c10d_functional.all_to_all_single(
        input,
        output_split_sizes,
        input_split_sizes,
        group_name,
    )

