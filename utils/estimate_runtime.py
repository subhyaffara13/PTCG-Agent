
def estimate_runtime(node: fx.Node) -> float:
    RUNTIME_MODE = config.activation_memory_budget_runtime_estimator

    def materialize_arg(x: Any) -> Any:
        if isinstance(x, fx.Node) and isinstance(x.meta["val"], torch.Tensor):
            return _remove_symbols_without_guarding(x.meta["val"], fallback=4096)
        elif isinstance(x, fx.Node) and isinstance(x.meta["val"], torch.SymInt):
            return optimization_hint(x.meta["val"], fallback=4096)
        elif isinstance(x, fx.Node) and isinstance(x.meta["val"], torch.SymFloat):
            return 1.0
        elif isinstance(x, fx.Node) and isinstance(x.meta["val"], torch.SymBool):
            return True
        else:
            return x

    if RUNTIME_MODE == "testing":
        return 1

    elif RUNTIME_MODE == "profile":
        with no_dispatch():
            from torch._inductor.runtime.benchmarking import benchmarker

            args, kwargs = pytree.tree_map(materialize_arg, (node.args, node.kwargs))
            # pyrefly: ignore[not-callable]
            ms = benchmarker.benchmark_gpu(lambda: node.target(*args, **kwargs))
            return ms

    elif RUNTIME_MODE == "flops":
        # todo(chilli): Normalize this to also return ms
        from torch.utils.flop_counter import FlopCounterMode

        args, kwargs = pytree.tree_map(materialize_arg, (node.args, node.kwargs))
        with FlopCounterMode(display=False) as mode:
            # pyrefly: ignore[not-callable]
            node.target(*args, **kwargs)
        counted_flops = mode.get_total_flops()
        return max(counted_flops, 1)

    elif isinstance(RUNTIME_MODE, CustomRuntimeEstimator):
        return RUNTIME_MODE(node)

    else:
        raise RuntimeError(f"Not aware of runtime estimator: {RUNTIME_MODE}")

