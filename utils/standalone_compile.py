import copy
from typing import Any

def standalone_compile(
    gm: GraphModule,
    example_inputs: Sequence[InputType],
    *,
    dynamic_shapes: Any,
    options: Any,
    aot: bool = False,  # AOT mode, which uses BundledAOTAutogradCache
    donate_graph_module: bool = False,
) -> CompiledArtifact:
    """
    Implementation of torch.inductor.standalone_compile
    """
    from .compile_fx import compile_fx

    ignore_shape_env = _resolve_ignore_shape_env(dynamic_shapes)
    with _standalone_context(gm, dynamic_shapes, aot):
        # compile_fx takes ownership of gm and may mutate it on cache miss.
        if not donate_graph_module:
            gm = copy.deepcopy(gm)
        compiled_fn = compile_fx(
            gm, example_inputs, ignore_shape_env=ignore_shape_env, **options
        )
        assert callable(compiled_fn)
        if aot:
            if not hasattr(compiled_fn, "serialize"):
                raise RuntimeError(
                    "Compiled function should have serialize method when aot=True"
                )
            return AOTCompiledArtifact(compiled_fn)
        artifacts = torch.compiler.save_cache_artifacts()
        if artifacts is None:
            log.warning(
                "standalone_compile artifact generation failed, cannot save. "
                "Run with TORCH_LOGS=+torch._inductor.codecache to identify the problem"
            )

    return CacheCompiledArtifact(compiled_fn, artifacts)


def standalone_compile(
    gm: torch.fx.GraphModule,
    example_inputs: list[InputType],
    *,
    dynamic_shapes: Literal[
        "from_example_inputs", "from_tracing_context", "from_graph"
    ] = "from_graph",
    options: dict[str, Any] | None = None,
    aot: bool = False,  # AOT mode, which uses BundledAOTAutogradCache
    donate_graph_module: bool = False,
) -> CompiledArtifact:
    """
    Precompilation API for inductor.

    .. code-block:: python

        compiled_artifact = torch._inductor.standalone_compile(gm, args)
        compiled_artifact.save(path=path, format="binary")

        # Later on a new process
        loaded = torch._inductor.CompiledArtifact.load(path=path, format="binary")
        compiled_out = loaded(*args)

    Args:
        gm: Graph Module
        example_inputs: Inputs for the graph module
        dynamic_shapes: If "from_graph" (default), we will use the dynamic
            shapes in the passed-in graph module.
            If "from_tracing_context", we use the dynamic shape info in the
            ambient tracing context.
            If "from_example_inputs", we will specialize the graph on the
            example_inputs.
        options: Inductor compilation options
        donate_graph_module: If True, standalone_compile takes ownership of
            the graph module and may mutate it, avoiding an internal deepcopy.
            Defaults to False for backwards compatibility.

    Returns:
        CompiledArtifact that can be saved to disk or invoked directly.
    """
    from .standalone_compile import standalone_compile

    options = options if options else {}
    return standalone_compile(
        gm,
        example_inputs,
        dynamic_shapes=dynamic_shapes,
        options=options,
        aot=aot,
        donate_graph_module=donate_graph_module,
    )

