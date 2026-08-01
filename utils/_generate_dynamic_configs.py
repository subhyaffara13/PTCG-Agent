
def _generate_dynamic_configs(
    tensor_inputs: list[Buffer],
    config_generator: Callable[[dict[str, torch.Tensor]], list[CustomOpConfig]],
    op_overload: torch._ops.OpOverload,
    operation_name: str,
) -> list[CustomOpConfig]:
    """Generate configs dynamically based on input tensors at lowering time."""
    # Get parameter names from op schema instead of impl signature
    schema = op_overload._schema
    param_names = [arg.name for arg in schema.arguments if not arg.kwarg_only]

    with V.fake_mode:
        fake_tensors = [ir_node_to_tensor(inp) for inp in tensor_inputs]

    fake_tensors_dict = dict(zip(param_names, fake_tensors))

    configs = config_generator(fake_tensors_dict)

    if not isinstance(configs, (list, tuple)):
        raise TypeError(
            f"config_generator must return a list or tuple of CustomOpConfig, "
            f"got {type(configs)}"
        )
    if not configs:
        log.info(
            "config_generator returned empty list for %s, will use default lowering",
            operation_name,
        )
        return []

    return list(configs)

