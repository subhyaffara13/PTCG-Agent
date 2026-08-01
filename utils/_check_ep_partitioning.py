
def _check_ep_partitioning(
    model: onnx.ModelProto, supported_ops_config: pathlib.Path, require_fixed_input_sizes: bool, max_rank: int = 999
):
    supported_ops = _SupportedOpsChecker(supported_ops_config)
    partition_info = check_partitioning(model.graph, supported_ops, require_fixed_input_sizes, max_rank)
    return partition_info

