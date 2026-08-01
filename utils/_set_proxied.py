
def _set_proxied(const) -> nodes.ClassDef:
    # TODO : find a nicer way to handle this situation;
    return _CONST_PROXY[const.value.__class__]

