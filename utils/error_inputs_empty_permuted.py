
def error_inputs_empty_permuted(op_info, device, **kwargs):
    yield ErrorInput(
        SampleInput((2,), args=((0, 1),)),
        error_type=RuntimeError,
        error_regex="Number of dimensions in size does not match the length of the physical_layout"
    )
    yield ErrorInput(
        SampleInput((2,), args=((3,),)),
        error_type=RuntimeError,
        error_regex="Dimension out of range"
    )
    yield ErrorInput(
        SampleInput((2, 3), args=((0, 0),)),
        error_type=RuntimeError,
        error_regex="Duplicate dim not allowed"
    )

