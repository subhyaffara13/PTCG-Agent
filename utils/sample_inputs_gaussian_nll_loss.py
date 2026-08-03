import random

def sample_inputs_gaussian_nll_loss(op_info, device, dtype, requires_grad, **kwargs):
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    # Set low slightly above 0 so gradcheck doesn't accidentally dip below 0
    make_var = partial(make_tensor, low=0.1, device=device, dtype=dtype, requires_grad=requires_grad)

    def gen_shape(shape):
        yield shape
        # Broadcast
        yield (*shape[:-1], 1)
        yield shape[:-1]

    def gen_shape_kwargs():
        for s, r in _generate_sample_shape_reduction():
            for t_s, v_s in product(gen_shape(s), gen_shape(s)):
                yield _make_tensor(s), _make_tensor(t_s), make_var(v_s), dict(reduction=r)
                yield (
                    _make_tensor(s), _make_tensor(t_s), make_var(v_s),
                    dict(full=True, reduction=r)
                )
                yield (
                    _make_tensor(s), _make_tensor(t_s), make_var(v_s),
                    dict(eps=random.uniform(1e-6, 1e-3), reduction=r)
                )
                yield (
                    _make_tensor(s), _make_tensor(t_s), make_var(v_s),
                    dict(full=True, eps=random.uniform(1e-6, 1e-3), reduction=r)
                )

    for input, target, var, kwargs in gen_shape_kwargs():
        yield SampleInput(input, args=(target, var, ), kwargs=kwargs)

