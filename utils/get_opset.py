
def get_opset(mp, domain=None):
    domain = domain or ["", "onnx", "ai.onnx"]
    if type(domain) != list:  # noqa: E721
        domain = [domain]
    for opset in mp.opset_import:
        if opset.domain in domain:
            return opset.version

    return None

