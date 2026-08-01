
def get_module_weight(module):
    if type(module) in _supported_types:
        return module.weight
    else:
        return module[0].weight

