
def kldivloss_no_reduce_test():
    t = torch.rand(10, 10, dtype=torch.double)
    return dict(
        fullname='KLDivLoss_no_reduce',
        constructor=wrap_functional(
            lambda i: F.kl_div(i, t.type_as(i), reduction='none')),
        cpp_function_call='F::kl_div(i, t.to(i.options()), F::KLDivFuncOptions().reduction(torch::kNone))',
        input_fn=lambda: torch.rand(10, 10).log(),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_:
            loss_reference_fns['KLDivLoss'](i, t.type_as(i), reduction='none'),
        supports_forward_ad=True,
        pickle=False,
        default_dtype=torch.double,
    )

