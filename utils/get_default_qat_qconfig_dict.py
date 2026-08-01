
def get_default_qat_qconfig_dict(backend="x86", version=1):
    return torch.ao.quantization.get_default_qat_qconfig_mapping(
        backend, version
    ).to_dict()

