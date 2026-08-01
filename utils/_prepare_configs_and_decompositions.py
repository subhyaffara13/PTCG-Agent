
def _prepare_configs_and_decompositions(
    processed_configs: list[CustomOpConfig] | None,
    config_generator: Callable[[dict[str, torch.Tensor]], list[CustomOpConfig]] | None,
    tensor_inputs: list[Any],
    default_impl: Callable[..., Any],
    op_overload: torch._ops.OpOverload,
    runtime_kwargs: dict[str, Any],
    name: str,
) -> tuple[list[Callable], list[dict[str, Any]], list[dict[str, Any]]]:
    """Prepare decompositions and merged kwargs from configs.

    Handles both static configs and dynamic config generation.
    Merges config params with runtime kwargs (runtime takes precedence).
    """
    # Get configs: either generate dynamically or use static configs
    if config_generator is not None:
        configs_to_use = _generate_dynamic_configs(
            tensor_inputs, config_generator, op_overload, name
        )
    else:
        assert processed_configs is not None
        configs_to_use = processed_configs

    # Prepare decompositions and kwargs for autotuning
    decompositions = []
    non_tensor_args = []
    config_patches_list = []

    for cfg in configs_to_use:
        decomp = cfg.get_decomposition(default_impl=default_impl)
        decompositions.append(decomp)

        # Merge config params with runtime kwargs (runtime takes precedence)
        merged_kwargs = _merge_config_and_runtime_kwargs(cfg.params, runtime_kwargs)
        non_tensor_args.append(merged_kwargs)

        # Collect config_patches for each config
        config_patches_list.append(cfg.config_patches)

    return decompositions, non_tensor_args, config_patches_list

