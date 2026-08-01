
def l1loss_no_reduce_test():
    t = torch.randn(2, 3, 4, dtype=torch.double)
    return dict(
        fullname='L1Loss_no_reduce',
        constructor=wrap_functional(
            lambda i: F.l1_loss(i, t.type_as(i), reduction='none')),
        cpp_function_call='F::l1_loss(i, t.to(i.options()), F::L1LossFuncOptions().reduction(torch::kNone))',
        input_fn=lambda: torch.randn(2, 3, 4),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_: (i - t.type_as(i)).abs(),
        supports_forward_ad=True,
        pickle=False,
        default_dtype=torch.double)

