
def maybe_warning_due_to_dynamic_shape(
    fn_cache: dict[tuple[int, ...], Callable[..., Any]],
    new_int_key: Any,
) -> bool:
    num_cudagraphs = len(fn_cache.keys()) + 1

    def warn_msg() -> str:
        return (
            "CUDAGraph supports dynamic shapes by recording a new graph for each "
            "distinct input size. Recording too many CUDAGraphs may lead to "
            f"extra overhead. We have observed {num_cudagraphs} distinct sizes. "
            "Please consider the following options for better performance: "
            "a) padding inputs to a few fixed number of shapes; or b) set "
            "torch._inductor.config.triton.cudagraph_skip_dynamic_graphs=True. "
            "Set torch._inductor.config.triton.cudagraph_dynamic_shape_warn_limit=None "
            "to silence this warning."
        )

    if (
        torch._inductor.config.triton.cudagraph_dynamic_shape_warn_limit
        and num_cudagraphs
        > torch._inductor.config.triton.cudagraph_dynamic_shape_warn_limit
    ):
        cudagraphs_log.warning(warn_msg())
        return True

    return False

