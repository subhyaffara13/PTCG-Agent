
def bceloss_weights_no_reduce_test():
    t = Variable(torch.randn(15, 10, dtype=torch.double).gt(0).to(torch.double))
    weights = torch.rand(10, dtype=torch.double)
    return dict(
        fullname='BCELoss_weights_no_reduce',
        constructor=wrap_functional(
            lambda i: F.binary_cross_entropy(i, t.type_as(i),
                                             weight=weights.type_as(i), reduction='none')),
        cpp_function_call='F::binary_cross_entropy('
                          'i, t.to(i.options()), '
                          'F::BinaryCrossEntropyFuncOptions().weight(weights.to(i.options())).reduction(torch::kNone))',
        input_fn=lambda: torch.rand(15, 10).clamp_(2.8e-2, 1 - 2.8e-2),
        cpp_var_map={'i': '_get_input()', 't': t, 'weights': weights},
        reference_fn=lambda i, p, m: -(t * i.log() + (1 - t) * (1 - i).log()) * weights,
        pickle=False,
        precision=3e-4,
        default_dtype=torch.double,
    )

