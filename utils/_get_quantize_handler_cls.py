
def _get_quantize_handler_cls(
    observation_type: ObservationType,
    dtype_configs: list[DTypeConfig],
    num_tensor_args_to_observation_type: dict[int, ObservationType],
) -> type[QuantizeHandler]:
    """
    Return a configurable QuantizeHandler that matches the given specifications from the backend.
    """

    class ConfigurableQuantizeHandler(QuantizeHandler):
        def __init__(
            self,
            node_pattern: NodePattern,
            modules: dict[str, torch.nn.Module],
            root_node_getter: Callable | None = None,
        ):
            super().__init__(node_pattern, modules, root_node_getter)
            if num_tensor_args_to_observation_type:
                if self.num_tensor_args not in num_tensor_args_to_observation_type:
                    raise AssertionError(
                        f"Must provide observation_type config for tensor number {self.num_tensor_args}"
                        f" in num_tensor_args_to_observation_type for {node_pattern}"
                    )
                self.observation_type = num_tensor_args_to_observation_type[
                    self.num_tensor_args
                ]
            else:
                self.observation_type = observation_type
            self.dtype_configs = dtype_configs

        def is_general_tensor_value_op(self) -> bool:
            return (
                self.observation_type
                == ObservationType.OUTPUT_SHARE_OBSERVER_WITH_INPUT
            )

    return ConfigurableQuantizeHandler

