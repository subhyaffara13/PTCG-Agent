
def has_bias(module) -> bool:
    if type(module) in _supported_types:
        return module.bias is not None
    else:
        return module[0].bias is not None

