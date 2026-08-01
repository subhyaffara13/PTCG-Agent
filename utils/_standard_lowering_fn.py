
def _standard_lowering_fn(
    processed_configs: list[CustomOpConfig],
    default_impl: Callable[..., Any],
    name: str,
    op_overload: torch._ops.OpOverload,
    input_gen_fns: dict[str, Callable[[torch.Tensor], torch.Tensor]] | None,
    tensor_inputs: list[Any],
    runtime_kwargs: dict[str, Any],
    config_generator: Callable[[dict[str, torch.Tensor]], list[CustomOpConfig]]
    | None = None,
    min_speedup_threshold: float = 1.0,
    benchmark_with_cudagraphs: bool = False,
) -> Any:
    """Standard autotuning lowering function.

    Returns None if no configs/decompositions available, signaling caller to
    use normal lowering.
    """
    decompositions, non_tensor_args, config_patches_list = (
        _prepare_configs_and_decompositions(
            processed_configs,
            config_generator,
            tensor_inputs,
            default_impl,
            op_overload,
            runtime_kwargs,
            name,
        )
    )

    # If no decompositions, signal caller to use normal lowering
    if not decompositions:
        return None

    result, _ = autotune_custom_op(
        name=name,
        decompositions=decompositions,
        inputs=tensor_inputs,
        non_tensor_args=non_tensor_args,
        config_patches_list=config_patches_list,
        op_overload=op_overload,
        user_input_gen_fns=input_gen_fns,
        min_speedup_threshold=min_speedup_threshold,
        benchmark_with_cudagraphs=benchmark_with_cudagraphs,
    )

    validate_ir(result)
    return result

