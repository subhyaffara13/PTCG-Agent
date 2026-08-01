
def constrain_to_fake_tensors(args, kwargs, fake_args, fake_kwargs):
    args = tuple(
        constrain_to_fake_tensor(arg, fake_arg)
        for arg, fake_arg in zip(args, fake_args)
    )
    kwargs = {k: constrain_to_fake_tensor(v, fake_kwargs[k]) for k, v in kwargs.items()}
    return args, kwargs

