
def _get_symmetric_qnnpack_qconfig_mapping() -> QConfigMapping:
    """
    Return a QConfigMapping that uses `torch.ao.quantization.default_symmetric_qnnpack_qconfig`
    as the default QConfig.
    """
    default_qconfig = default_symmetric_qnnpack_qconfig
    return _get_default_qconfig_mapping_with_default_qconfig(
        False, "qnnpack", default_qconfig
    )

