
def sample_inputs_trilu_indices(op_info, device, dtype, requires_grad, **kwargs):
    # (row, col, offset)
    args_list = ((0, 0),
                 (20, 0),
                 (0, 20),
                 (20, 21, 0),
                 (20, 21, 7),
                 (20, 21, -7),
                 # Large test cases below are deliberately commented out to speed up CI
                 # tests and to avoid OOM error. When modifying implementations of
                 # tril_indices and triu_indices, please enable these tests and make sure
                 # they pass.
                 # (2, 68435455, 3),
                 # (5000, 5000),
                 # (5000, 5000, 1234),
                 # (5000, 5000, -1233),
                 )
    for args in args_list:
        yield SampleInput(args[0], args=args[1:], kwargs={"dtype": dtype, "device": device})

