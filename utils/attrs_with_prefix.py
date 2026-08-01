
def attrs_with_prefix(module, prefix):
    return [x for x, _ in module._modules._c.items()
            if x.startswith(prefix)]

