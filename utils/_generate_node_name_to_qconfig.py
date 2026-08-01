
def _generate_node_name_to_qconfig(
    root: torch.nn.Module,
    modules: dict[str, torch.nn.Module],
    input_graph: Graph,
    qconfig_mapping: QConfigMapping,
    node_name_to_scope: dict[str, tuple[str, type]],
) -> dict[str, QConfigAny]:
    global_qconfig = qconfig_mapping.global_qconfig
    node_name_to_qconfig = {}

    # example:
    #
    #   {'foo.bar': {F.linear: 0, F.conv2d: 1, ...}, ...}
    #
    # meaning in submodule 'foo.bar', we have seen 0 F.linear and
    # 1 F.conv2d invocations so far.
    submodule_to_object_type_to_cur_idx: dict[str, dict[Callable, int]] = defaultdict(
        lambda: defaultdict(int)
    )
    for node in input_graph.nodes:
        qconfig = None
        if node.op == "get_attr":
            module_name, _ = _parent_name(node.target)
            qconfig = _maybe_adjust_qconfig_for_module_type_or_name(
                qconfig_mapping, type(modules[module_name]), module_name, global_qconfig
            )
            qconfig_with_device_check = _add_module_to_qconfig_obs_ctr(
                qconfig, modules.get(node.target)
            )
        elif node.op == "call_function":
            # precedence: module_name_qconfig
            # > function_qconfig > global_qconfig
            # module_name takes precedence over function qconfig
            function_qconfig = _get_object_type_qconfig(
                qconfig_mapping, node.target, global_qconfig
            )
            module_path, module_type = node_name_to_scope[node.name]
            qconfig = _maybe_adjust_qconfig_for_module_type_or_name(
                qconfig_mapping, module_type, module_path, function_qconfig
            )

            cur_object_type_idx = submodule_to_object_type_to_cur_idx[module_path][
                node.target
            ]
            submodule_to_object_type_to_cur_idx[module_path][node.target] += 1
            qconfig = _maybe_adjust_qconfig_for_module_name_object_type_order(
                qconfig_mapping, module_path, node.target, cur_object_type_idx, qconfig
            )
            qconfig_with_device_check = _add_module_to_qconfig_obs_ctr(
                qconfig, modules.get(node.target)
            )

        elif node.op == "call_method":
            module_path, module_type = node_name_to_scope[node.name]
            # first use node.target (string) to get the qconfig
            # this is to support configs like
            # "object_type": [("reshape", qconfig)]
            qconfig = _maybe_adjust_qconfig_for_module_type_or_name(
                qconfig_mapping, node.target, module_path, global_qconfig
            )
            # if there is no special config for the method, we'll fall back to the
            # config for the module that contains the call_method node
            qconfig = _maybe_adjust_qconfig_for_module_type_or_name(
                qconfig_mapping, module_type, module_path, qconfig
            )
            # currently call_method does not support modifying qconfig
            # by order, we can add this later if it is needed.
            qconfig_with_device_check = _add_module_to_qconfig_obs_ctr(
                qconfig, modules.get(node.target)
            )

        elif node.op == "call_module":
            # if the node is an observer, just continue - don't add it to the qconfig_map
            if _is_activation_post_process(modules[node.target]):
                continue
            qconfig = _maybe_adjust_qconfig_for_module_type_or_name(
                qconfig_mapping, type(modules[node.target]), node.target, global_qconfig
            )

            module_path, module_type = node_name_to_scope[node.name]
            # Note: for call_module, the module_path is the current module's name.
            # to meaningfully count invocations, we need to count them in the parent
            # module.
            parent_name, _ = _parent_name(module_path)
            cur_object_type_idx = submodule_to_object_type_to_cur_idx[parent_name][
                module_type
            ]
            submodule_to_object_type_to_cur_idx[parent_name][module_type] += 1
            qconfig = _maybe_adjust_qconfig_for_module_name_object_type_order(
                qconfig_mapping, parent_name, module_type, cur_object_type_idx, qconfig
            )
            qconfig_with_device_check = _add_module_to_qconfig_obs_ctr(
                qconfig, modules.get(node.target)
            )

            # regex is not supported eager mode propagate_qconfig_, we'll
            # need to set the qconfig explicitly here in case regex
            # is used
            modules[node.target].qconfig = qconfig_with_device_check
        else:
            qconfig_with_device_check = None

        node_name_to_qconfig[node.name] = qconfig_with_device_check
    return node_name_to_qconfig

