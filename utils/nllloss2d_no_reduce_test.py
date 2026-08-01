
def nllloss2d_no_reduce_test():
    t = Variable(torch.rand(2, 5, 5).mul(3).floor().long())
    kwargs = {'reduction': 'none'}
    return dict(
        fullname='NLLLoss2d_no_reduce',
        constructor=wrap_functional(
            lambda i: F.nll_loss(i, t.type_as(i).long(), reduction=kwargs['reduction'])),
        cpp_function_call='''F::nll_loss(
            i, t.to(i.options()).to(torch::kLong), F::NLLLossFuncOptions().reduction(torch::kNone))''',
        input_fn=lambda: torch.rand(2, 3, 5, 5).log(),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_:
            loss_reference_fns['NLLLossNd'](i, t.type_as(i).long(), **kwargs),
        pickle=False,
        default_dtype=torch.double)

