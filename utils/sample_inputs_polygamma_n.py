
def sample_inputs_polygamma_n(n):
    return partial(sample_inputs_elementwise_njt_unary, op_kwargs={"n": n})

