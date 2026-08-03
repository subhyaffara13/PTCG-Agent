from typing import Callable

def _add_shadow_loggers_impl(
    name_a: str,
    gm_a: GraphModule,
    name_b: str,
    gm_b: GraphModule,
    logger_cls: Callable,
    should_log_inputs: bool,
    base_name_to_sets_of_related_ops: dict[str, set[NSNodeTargetType]] | None = None,
    node_type_to_io_type_map: dict[str, set[NSNodeTargetType]] | None = None,
    unmatchable_types_map: dict[str, set[NSNodeTargetType]] | None = None,
) -> nn.Module:
    torch._C._log_api_usage_once(
        "quantization_api._numeric_suite_fx._add_shadow_loggers_impl"
    )
    matched_subgraph_pairs = get_matching_subgraph_pairs(
        gm_a, gm_b, base_name_to_sets_of_related_ops, unmatchable_types_map
    )
    gm_a_shadows_b = create_a_shadows_b(
        name_a,
        gm_a,
        name_b,
        gm_b,
        matched_subgraph_pairs,
        logger_cls,
        should_log_inputs=should_log_inputs,
        node_type_to_io_type_map=node_type_to_io_type_map,
    )
    return gm_a_shadows_b

