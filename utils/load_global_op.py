
def load_global_op(name: str, type: RType, src: str) -> LoadAddressDescription:
    assert name not in global_names, "already defined: %s" % name
    global_names[name] = (type, src)
    return LoadAddressDescription(name, type, src)

