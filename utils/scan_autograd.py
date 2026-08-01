
def scan_autograd(combine_fn, init, xs, additional_inputs):
    with disable_proxy_modes_tracing():
        hop_partitioned_graph: HopPartitionedGraph = (
            HopGraphMinCutPartitioner.create_partitioned_graph(
                combine_fn,
                (*init, *[x[0] for x in xs], *additional_inputs),
                always_recompute_complex_exprs=True,
            )
        )

    return ScanAutogradOp.apply(
        hop_partitioned_graph,
        len(init),
        len(xs),
        len(additional_inputs),
        *init,
        *xs,
        *additional_inputs,
    )

