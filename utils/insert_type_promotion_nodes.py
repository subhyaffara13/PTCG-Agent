
def insert_type_promotion_nodes(
    graph_module: torch.fx.GraphModule,
) -> None:
    """Inplace pass to insert explicit type promotion nodes, recursively through nested modules."""
    for module in graph_module.modules():
        if not isinstance(module, torch.fx.GraphModule):
            raise AssertionError(f"Expected GraphModule, got {type(module)}")
        passes.InsertTypePromotion(module).run()

