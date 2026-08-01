
def error_inputs_multinomial(op_info, device, **kwargs):
    dtype = highest_precision_float(device)
    x = torch.empty(1, 2, 3, dtype=dtype, device=device)
    yield ErrorInput(SampleInput(x, args=(2,)),
                     error_regex="prob_dist must be 1 or 2 dim")

    x = torch.empty(1, 2, dtype=torch.long, device=device)
    yield ErrorInput(SampleInput(x, args=(2,)),
                     error_regex="multinomial only supports floating-point dtypes for input")

    x = torch.empty(1, 2, dtype=dtype, device=device)
    y = torch.empty(1, 2, dtype=dtype, device=device)
    yield ErrorInput(SampleInput(x, args=(2,), kwargs=dict(out=y)),
                     error_regex="multinomial expects Long tensor out")

    x = torch.empty(2, dtype=dtype, device=device)
    yield ErrorInput(SampleInput(x, args=(0,)),
                     error_regex="cannot sample n_sample <= 0 samples")

    x = torch.empty(2, dtype=dtype, device=device)
    yield ErrorInput(SampleInput(x, args=(-1,)),
                     error_regex="cannot sample n_sample <= 0 samples")

    x = torch.empty(2, dtype=dtype, device=device)
    yield ErrorInput(SampleInput(x, args=(3, False,)),
                     error_regex="cannot sample n_sample > prob_dist")

    x = torch.empty(16777217, dtype=dtype, device=device)
    yield ErrorInput(SampleInput(x, args=(3,)),
                     error_regex="number of categories cannot exceed")

    inputs = ((1., -1., 1.), (1., inf, 1.), (1., -inf, 1.), (1., 1., nan))

    err_msg1 = "probability tensor contains either `inf`, `nan` or element < 0"
    err_msg2 = "invalid multinomial distribution"

    rep_arg = (False, True) if torch.device(device).type == 'cpu' else (False,)

    if torch.device(device).type == 'cpu':
        for rep in rep_arg:
            kwargs = {'num_samples': 2, 'replacement': rep}

            for shape in inputs:
                # error case when input tensor contains `inf`, `nan` or negative element
                yield ErrorInput(SampleInput(torch.tensor(shape), kwargs=kwargs),
                                 error_regex=err_msg1 if rep is False else err_msg2)

            # error case for the invalid multinomial distribution (sum of probabilities <= 0), 1-D input
            x = torch.zeros(3, device=device)
            yield ErrorInput(SampleInput(x, kwargs=kwargs),
                             error_regex=err_msg2)

            # error case for the invalid multinomial distribution (sum of probabilities <= 0), 2-D input
            x = torch.zeros(3, 3, device=device)
            yield ErrorInput(SampleInput(x, kwargs=kwargs),
                             error_regex=err_msg2)

            # error case for the invalid multinomial distribution
            x[1, :] = 1
            yield ErrorInput(SampleInput(x, kwargs=kwargs),
                             error_regex=err_msg2)

