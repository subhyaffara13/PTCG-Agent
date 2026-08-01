
def estimate_nccl_collective_runtime(node: ir.IRNode) -> float:
    """
    Returns estimated NCCL collective runtime in nanoseconds (ms).

    The following heuristics are copied from https://github.com/NVIDIA/nccl/blob/master/src/graph/tuning.cc.
    We aim to estimate the runtime as accurately as possible.

    Assumptions:
    - only ring algorithm (NCCL_ALGO_RING) is used
    - only Low-Latency protocol (NCCL_PROTO_LL) is used, i.e. Simple or LL128 is not used
    - 8 gpus per node  # TODO: Need to find a way to get accurate "gpus per node" and "# nodes" info.
    - collective is one of: allreduce, reducescatter, allgather
    """
    tensor_storage_size_bytes = get_collective_input_size_bytes(node)
    group_size = get_collective_group_size(node)
    coll = get_collective_type(node)
    return estimate_nccl_collective_runtime_impl(
        tensor_storage_size_bytes, group_size, coll
    )

