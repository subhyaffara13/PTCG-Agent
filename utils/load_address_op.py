
def load_address_op(name: str, type: RType, src: str) -> LoadAddressDescription:
    assert name not in builtin_names, "already defined: %s" % name
    builtin_names[name] = (type, src)
    return LoadAddressDescription(name, type, src)

