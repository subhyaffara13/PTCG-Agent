
def _is_valid_module(qname):
    spec = importlib.util.find_spec(qname)
    return spec is not None

