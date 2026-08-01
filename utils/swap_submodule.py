
def swap_submodule(
    module: "torch.nn.Module",
    name: str,
    submodule: "torch.nn.Module",
) -> "torch.nn.Module":
    if not isinstance(module, torch.nn.Module):
        raise TypeError(f"{module} is not an instance of torch.nn.Module")
    if not isinstance(submodule, torch.nn.Module):
        raise TypeError(f"{submodule} is not an instance of torch.nn.Module")
    if "." in name:
        raise KeyError('submodule name can\'t contain "."')
    if name == "":
        raise KeyError('submodule name can\'t be empty string ""')
    if name not in module._modules:
        raise KeyError(f"submodule {name} does not exist")

    orig_submodule = module._modules[name]
    if not isinstance(orig_submodule, torch.nn.Module):
        raise TypeError(f"{name} attribute is not an instance of torch.nn.Module")
    module._modules[name] = submodule
    return orig_submodule

