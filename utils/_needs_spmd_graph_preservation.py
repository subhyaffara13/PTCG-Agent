
def _needs_spmd_graph_preservation() -> bool:
    """Check if SPMD graph preservation is needed for distributed overlap."""
    return (
        config.aten_distributed_optimizations.enable_overlap_scheduling
        or config.reorder_for_compute_comm_overlap
    )

