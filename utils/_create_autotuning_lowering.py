
def _create_autotuning_lowering(
    processed_configs: list[CustomOpConfig],
    default_impl: Callable[..., Any],
    name: str,
    op_overload: torch._ops.OpOverload,
    input_gen_fns: dict[str, Callable[[torch.Tensor], torch.Tensor]] | None,
    range_upper_bound: int,
    is_range_based: bool = False,
    config_generator: Callable[[dict[str, torch.Tensor]], list[CustomOpConfig]]
    | None = None,
    dispatch_on: tuple[str, int] | None = None,
    split_points: list[int] | None = None,
    min_speedup_threshold: float = 1.0,
    benchmark_with_cudagraphs: bool = False,
) -> Callable[..., Any]:
    """Create the lowering function for autotuning."""
    if not is_range_based:
        # Standard autotuning path
        @functools.wraps(op_overload)
        def standard_lowering_wrapper(*args: Any, **kwargs: Any) -> Any:
            tensor_inputs, runtime_kwargs = _extract_tensor_inputs(
                args, kwargs, op_overload
            )
            return _standard_lowering_fn(
                processed_configs=processed_configs,
                default_impl=default_impl,
                name=name,
                op_overload=op_overload,
                input_gen_fns=input_gen_fns,
                tensor_inputs=tensor_inputs,
                runtime_kwargs=runtime_kwargs,
                config_generator=config_generator,
                min_speedup_threshold=min_speedup_threshold,
                benchmark_with_cudagraphs=benchmark_with_cudagraphs,
            )

        return standard_lowering_wrapper

    # Range-based autotuning path
    # pyrefly: ignore [not-iterable]
    tensor_name, dim_index = dispatch_on
    # pyrefly: ignore [bad-argument-type]
    ranges = _create_ranges_from_split_points(split_points)

    @functools.wraps(op_overload)
    def range_based_lowering_wrapper(*args: Any, **kwargs: Any) -> Any:
        tensor_inputs, runtime_kwargs = _extract_tensor_inputs(
            args, kwargs, op_overload
        )
        return _range_based_lowering_fn(
            processed_configs=processed_configs,
            default_impl=default_impl,
            name=name,
            op_overload=op_overload,
            input_gen_fns=input_gen_fns,
            tensor_name=tensor_name,
            dim_index=dim_index,
            ranges=ranges,
            tensor_inputs=tensor_inputs,
            runtime_kwargs=runtime_kwargs,
            range_upper_bound=range_upper_bound,
            config_generator=config_generator,
            min_speedup_threshold=min_speedup_threshold,
            benchmark_with_cudagraphs=benchmark_with_cudagraphs,
        )

    return range_based_lowering_wrapper

