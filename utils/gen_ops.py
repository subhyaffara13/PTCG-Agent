
def gen_ops(device_type: str) -> dict[Any, Any]:
    """
    Generates all supported CUTLASS operations.
    """
    with dynamo_timed("cutlass_utils.gen_ops"):
        arch = cutlass_arch(device_type)
        version = toolkit_version(device_type)
        return _gen_ops_cached(arch, version, device_type)

