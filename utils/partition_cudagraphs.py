
def partition_cudagraphs(gm, inputs):
    """
    Partition an FX graph into sub-GraphModules that can be validly run under
    CUDA graphs.  For a subgraph to be runnable under CUDA, all of the operations
    must involve CUDA tensors only/
    """

    FakeTensorProp(gm).propagate(*inputs)
    supported_ops = CudaGraphsSupport()
    # TODO: single node partition may be wrong due to the pessimization
    # from copying in and out the data.  Check in benchmarks, perhaps
    partitioner = CapabilityBasedPartitioner(
        gm, supported_ops, allows_single_node_partition=True
    )
    partitions = partitioner.propose_partitions()
    fused_graph = partitioner.fuse_partitions(partitions)
    return fused_graph

