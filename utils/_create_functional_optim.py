
def _create_functional_optim(functional_optim_cls: type, *args, **kwargs):
    return functional_optim_cls(
        [],
        *args,
        **kwargs,
        _allow_empty_param_list=True,
    )

