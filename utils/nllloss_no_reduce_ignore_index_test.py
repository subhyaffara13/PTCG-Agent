
def nllloss_no_reduce_ignore_index_test():
    t = Variable(torch.empty(15).uniform_().mul(10).floor().long())
    kwargs: dict[str, int | str] = {'ignore_index': 2, 'reduction': 'none'}
    return dict(
        fullname='NLLLoss_no_reduce_ignore_index',
        constructor=wrap_functional(
            lambda i: F.nll_loss(i, t.type_as(i).long(), ignore_index=int(kwargs['ignore_index']),
                                 reduction=str(kwargs['reduction']))),
        cpp_function_call='''F::nll_loss(
            i, t.to(i.options()).to(torch::kLong), F::NLLLossFuncOptions().ignore_index(2).reduction(torch::kNone))''',
        input_fn=lambda: torch.rand(15, 10).log(),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_:
            loss_reference_fns['NLLLoss'](i, t.type_as(i).long(), **kwargs),
        pickle=False,
        default_dtype=torch.double)

