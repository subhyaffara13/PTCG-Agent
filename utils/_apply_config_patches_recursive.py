
def _apply_config_patches_recursive(
    operations: list,
    config_patches: dict[str, Any],
) -> None:
    """Apply config_patches to operations, including those inside subgraphs."""
    for op in operations:
        if hasattr(op, "set_config_patches"):
            op.set_config_patches(config_patches.copy())

        # Recurse into any subgraphs (Conditional, WhileLoop, InvokeSubgraph, etc.)
        for subgraph in op.get_subgraphs():
            if subgraph.graph:
                _apply_config_patches_recursive(
                    subgraph.graph.operations, config_patches
                )

