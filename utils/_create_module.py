
def _create_module(module_cls, args, kwargs, device):
    module = module_cls(*args, **kwargs)
    if not isinstance(module, nn.Module):
        raise ValueError(
            "Expect `module_cls(*args, **kwargs)` returns an instance of <class nn.Module>, "
            f"but it returns an instance of {type(module)}."
        )
    module.to(device)
    return module

