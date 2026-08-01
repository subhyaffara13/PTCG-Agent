
def get_module_bias(module):
    if type(module) in _supported_types:
        return module.bias
    else:
        return module[0].bias

