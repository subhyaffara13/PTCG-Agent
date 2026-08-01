
def get_default_qconfig_dict(backend="x86", version=0):
    return torch.ao.quantization.get_default_qconfig_mapping(backend, version).to_dict()

