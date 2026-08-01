
def _all_to_all_single_meta(
    input, output_split_sizes, input_split_sizes, *args, **kwargs
):
    if output_split_sizes is None:
        return input.new_empty(input.size())
    else:
        for s in output_split_sizes:
            torch._check(s >= 0)
        out_size = list(input.size())
        out_size[0] = sum(output_split_sizes)
        return input.new_empty(out_size)

