
def scale_input_observer(node: Node, modules: dict[str, nn.Module]) -> None:
    """Scales the following input quantization observer's min/max values by
    updating the values with the scaled min/max values calculated by the input
    equalization observer
    """
    input_eq_obs = modules[str(node.target)]
    if not isinstance(input_eq_obs, _InputEqualizationObserver):
        raise AssertionError(
            "Expected the module at node.target to be an _InputEqualizationObserver"
        )

    input_quant_obs_node = node.args[0]
    if not isinstance(input_quant_obs_node, Node):
        raise AssertionError(
            "Expected the input quantization observer node to be a Node"
        )

    input_quant_obs = modules[str(input_quant_obs_node.target)]
    if not isinstance(input_quant_obs, ObserverBase):
        return

    min_input_scaled, max_input_scaled = input_eq_obs.calculate_scaled_minmax()
    if min_input_scaled is None and max_input_scaled is None:
        return
    input_quant_obs.min_val = min_input_scaled
    input_quant_obs.max_val = max_input_scaled

