from typing import Any

def _save_state(
    observed: GraphModule,
    node_name_to_qconfig: dict[str, QConfigAny],
    node_name_to_scope: dict[str, tuple[str, type]],
    prepare_custom_config: PrepareCustomConfig,
    equalization_node_name_to_qconfig: dict[str, Any],
    qconfig_mapping: QConfigMapping,
    is_qat: bool,
    observed_node_names: set[str],
) -> None:
    observed.meta["_observed_graph_module_attrs"] = ObservedGraphModuleAttrs(
        node_name_to_qconfig=node_name_to_qconfig,
        node_name_to_scope=node_name_to_scope,
        prepare_custom_config=prepare_custom_config,
        equalization_node_name_to_qconfig=equalization_node_name_to_qconfig,
        qconfig_mapping=qconfig_mapping,
        is_qat=is_qat,
        observed_node_names=observed_node_names,
    )

