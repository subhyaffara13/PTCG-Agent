
def sample_inputs_poisson_nll_loss(op_info, device, dtype, requires_grad, **kwargs):
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def gen_shape_kwargs():
        for s, r in _generate_sample_shape_reduction():
            for li in (True, False):
                for f in (True, False):
                    i1 = _make_tensor(s)
                    i2 = _make_tensor(s)
                    # For Poisson NLL Loss,
                    # target is assumed to be from
                    # Poisson Distribution which
                    # always has positive samples
                    t1 = _make_tensor(s, low=0)
                    t2 = _make_tensor(s, low=0)

                    if not li:
                        i1.abs_()
                        i2.abs_()
                    t1.abs_()
                    t2.abs_()

                    yield (
                        i1, t1,
                        dict(log_input=li, full=f, reduction=r)
                    )
                    yield (
                        i2, t2,
                        dict(log_input=li, full=f,
                             eps=random.uniform(1e-8, 1e-3),
                             reduction=r)
                    )

    for input, target, kwargs in gen_shape_kwargs():
        yield SampleInput(input, args=(target, ), kwargs=kwargs)

    # test INT_TO_FLOAT promotion
    if dtype.is_complex:
        for d in (torch.bool, torch.int64):
            yield SampleInput(_make_tensor(dtype=dtype), args=(_make_tensor(dtype=d),))
            yield SampleInput(_make_tensor(dtype=d), args=(_make_tensor(dtype=dtype),))

