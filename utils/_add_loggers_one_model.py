from typing import Callable

def _add_loggers_one_model(
    model_name: str,
    model: GraphModule,
    nodes_and_names_to_instrument_inputs: list[tuple[Node, str, str]],
    nodes_and_names_to_instrument_outputs: list[tuple[Node, str, str]],
    logger_cls: Callable,
) -> nn.Module:
    torch._C._log_api_usage_once(
        "quantization_api._numeric_suite_fx._add_loggers_one_model"
    )

    # TODO(future PR): do not observe nodes we do not care
    #   about (both fp32, denylist, etc)
    node_to_instrument_inputs_to_ref_name: dict[Node, tuple[str, str]] = {}
    node_to_instrument_outputs_to_ref_name: dict[Node, tuple[str, str]] = {}
    for node, ref_name, ref_node_type in nodes_and_names_to_instrument_inputs:
        node_to_instrument_inputs_to_ref_name[node] = (ref_name, ref_node_type)
    for node, ref_name, ref_node_type in nodes_and_names_to_instrument_outputs:
        node_to_instrument_outputs_to_ref_name[node] = (ref_name, ref_node_type)

    model = add_loggers_to_model(
        model,
        node_to_instrument_inputs_to_ref_name,
        node_to_instrument_outputs_to_ref_name,
        logger_cls,
        model_name,
    )
    return model

