
def poissonnllloss_no_reduce_test():
    t = torch.randn(10, 10)
    return dict(
        fullname='PoissonNLLLoss_no_reduce',
        constructor=wrap_functional(
            lambda i: F.poisson_nll_loss(i, t.type_as(i), reduction='none')),
        cpp_function_call='F::poisson_nll_loss('
                          'i, t.to(i.options()), F::PoissonNLLLossFuncOptions().reduction(torch::kNone))',
        input_fn=lambda: torch.rand(10, 10),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_: i.exp() - t.mul(i),
        pickle=False,
        default_dtype=torch.double)

