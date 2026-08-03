import time

def gen_mkl_autotuner(example_inputs, iters=10, warmup=1):
    """
    This generates a heuristic that can be passed into `optimize_for_inference` that
    determines whether a subgraph should be run in MKL by running it with the example_inputs.

    Example usage:
        heuristic = gen_mkl_autotuner(example_inputs, iters=10)
        fast_model = optimization.optimize_for_inference(model, heuristic)
    """
    fx_model = None
    old_modules = None

    def use_mkl_heuristic(graph: MklSubgraph) -> bool:
        nonlocal fx_model, old_modules
        input_nodes = graph.start_nodes
        if fx_model is None:
            fx_model = graph.fx_graph.owning_module
            old_modules = graph.fx_graph.old_modules  # type: ignore[attr-defined]
            ShapeProp(fx_model).propagate(example_inputs)
        sample_inputs = [torch.randn(node.shape) for node in input_nodes]  # type: ignore[attr-defined]
        output_args = cast(list[fx.Node], [node.args[0] for node in graph.end_nodes])
        submodule = extract_subgraph(fx_model, graph.nodes, input_nodes, output_args)

        def benchmark(f):
            for _ in range(warmup):
                f()
            begin = time.time()
            for _ in range(iters):
                f()
            return time.time() - begin

        mkl_time = benchmark(
            lambda: [
                i.to_dense() for i in submodule(*[i.to_mkldnn() for i in sample_inputs])
            ]
        )

        reset_modules(
            submodule.graph.nodes,
            dict(submodule.named_modules()),
            # pyrefly: ignore [bad-argument-type]
            old_modules,
        )
        no_mkl_time = benchmark(lambda: submodule(*sample_inputs))
        return mkl_time < no_mkl_time

    return use_mkl_heuristic

