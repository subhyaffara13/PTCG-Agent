
def _adaptive_max_pool1d(
    input: Tensor,
    output_size: BroadcastingList1[int],
    return_indices: bool = False,
) -> Tensor:
    if has_torch_function_unary(input):
        return handle_torch_function(
            adaptive_max_pool1d,
            (input,),
            input,
            output_size,
            return_indices=return_indices,
        )
    return adaptive_max_pool1d_with_indices(input, output_size)[0]

