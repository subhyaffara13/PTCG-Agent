
def meta_median(input):
    output_shape = utils.compute_reduction_output_shape(
        input.shape, tuple(range(input.dim()))
    )
    return input.new_empty(output_shape)

