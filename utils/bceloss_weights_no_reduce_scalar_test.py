
def bceloss_weights_no_reduce_scalar_test():
    t = torch.randn(()).gt(0).to(torch.double)
    weights = torch.rand((), dtype=torch.double)
    return dict(
        fullname='BCELoss_weights_no_reduce_scalar',
        constructor=wrap_functional(
            lambda i: F.binary_cross_entropy(i, t.type_as(i),
                                             weight=weights.type_as(i), reduction='none')),
        cpp_function_call='''F::binary_cross_entropy(
            i, t.to(i.options()),
            F::BinaryCrossEntropyFuncOptions().weight(weights.to(i.options())).reduction(torch::kNone))''',
        cpp_var_map={'i': '_get_input()', 't': t, 'weights': weights},
        input_fn=lambda: torch.rand(()).clamp_(2.8e-2, 1 - 2.8e-2),
        reference_fn=lambda i, *_: -(t * i.log() + (1 - t) * (1 - i).log()) * weights,
        pickle=False,
        default_dtype=torch.double,
    )

