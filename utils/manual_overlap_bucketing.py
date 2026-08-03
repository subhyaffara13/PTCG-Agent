from typing import Any, Callable

def manual_overlap_bucketing(
    gm: torch.fx.GraphModule,
    module_bucket_plans: list[list[str] | str],
    insert_overlap_deps: bool = False,
    module_stack_fn: Callable[[fx.Node], list[tuple[str, type[Any]]]] | None = None,
    bucket_mode: BucketMode | None = None,
) -> torch.fx.GraphModule:
    """Schedule nodes based on user specifications in module_bucket_plans
    The manual overlapping consists of two steps:
    Step 1: bucket all-gather/reduce-scatter in each module in module_bucket_plans
    Step 2: reorder all-gather to overlap with last module_bucket &
        reorder reduce-scatter to overlap with next module_bucket
    TODO(ruisizhang123): allow users to explicitly specify which
        module_bucket they want to overlap.

    Args:
        gm: input graph module to optimize.
        module_bucket_plans: user specified FQNs
        module_stack_fn: Optional callable for extracting module hierarchy from nodes.
            Used to construct a GraphView for identifying nodes in module_bucket_plans.
            The module_class component of the returned tuples is not used by this pass.

            See the `module_stack_fn` parameter in `make_graph_view` (graph_view.py) for
            detailed documentation on signature, return format, and usage examples.
        bucket_mode: Bucket mode for collective bucketing. None uses default.
    """
    # decode abbreviated FQNs to actual FQNs
    overlapped_gm = ManualOverlapScheduler(
        gm,
        module_bucket_plans,
        insert_overlap_deps,
        module_stack_fn,
        bucket_mode=bucket_mode,
    ).run()
    overlapped_gm.recompile()
    return overlapped_gm

