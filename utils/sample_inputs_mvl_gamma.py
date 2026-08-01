
def sample_inputs_mvl_gamma(p):
    return partial(sample_inputs_elementwise_njt_unary, op_kwargs={"p": p})

