import time
from typing import Any, Callable

def aot_compile_joint_with_descriptors(
    jd: JointWithDescriptors,
    *,
    partition_fn: Callable[..., Any] = default_partition,
    fw_compiler: AOTDispatchCompiler = boxed_nop_preserve_node_meta,
    bw_compiler: AOTDispatchCompiler | None = boxed_nop_preserve_node_meta,
    serializable: bool = False,
) -> Callable[..., Any]:
    """
    Companion function for aot_export_joint_with_descriptors which compiles the joint
    graph into a callable function that follows a standard calling convention.
    params_flat all are arguments.

    Note: We do NOT instantiate the module; this gives you the flexibility to subclass it and
    customize its behavior without having to worry about FQN rebinding.

    Args:
        serializable: If True, configures the compilation to produce a serializable
            callable by leveraging AOTAutogradCache machinery. This sets up the
            necessary cache_info and patches config options required for serialization.
            When True, this function will always return a BundledAOTAutogradSerializableCallable.
    """
    # TODO: Consider if we should allow_in_graph the result by default.
    from torch._dynamo.aot_compile_types import (
        BundledAOTAutogradSerializableCallable,
        SerializableCallable,
    )
    from torch._functorch._aot_autograd.schemas import AOTAutogradCacheInfo
    from torch._guards import detect_fake_mode
    from torch._inductor.output_code import OutputCode

    fw_compiler = SerializableAOTDispatchCompiler(OutputCode, fw_compiler)

    cache_ctx = nullcontext()
    if serializable:
        jd._aot_state.aot_config.cache_info = AOTAutogradCacheInfo(
            jd.cache_hash(),
            time.time_ns(),
            forward_symints=[],
        )
        cache_ctx = torch._functorch.config.patch(
            {
                "strict_autograd_cache": True,
                "bundled_autograd_cache": True,
                "force_non_lazy_backward_lowering": True,
                "bypass_autograd_cache_key": True,
            }
        )

    # Set up a TracingContext if one isn't already available.
    # This is needed for compilers (like regional_inductor) that call
    # standalone_compile with dynamic_shapes="from_tracing_context".
    tracing_context = torch._guards.TracingContext.try_get()
    if tracing_context is None:
        fake_mode = detect_fake_mode(jd._aot_state.flat_args)
        if fake_mode is not None:
            tracing_context = torch._guards.TracingContext(fake_mode)
            tracing_ctx = torch._guards.tracing(tracing_context)
        else:
            tracing_ctx = nullcontext()
    else:
        tracing_ctx = nullcontext()

    with cache_ctx, tracing_ctx:
        compiled_fn, _ = aot_stage2_compile(
            jd._aot_state,
            jd._aot_graph_capture,
            partition_fn,
            fw_compiler,
            bw_compiler,
        )

    if not isinstance(compiled_fn, SerializableCallable) and hasattr(
        compiled_fn, "serialize"
    ):
        compiled_fn = BundledAOTAutogradSerializableCallable(compiled_fn)

    # Cribbed from torch/export/pt2_archive/_package.py
    @simple_wraps(compiled_fn)
    @torch._dynamo.nonstrict_trace  # allow recursive compilation
    def unflattened_compiled_fn(*args: Any, **kwargs: Any) -> Any:
        flat_inputs = pytree.tree_flatten((args, reorder_kwargs(kwargs, jd.in_spec)))[0]
        # TODO: do I need to filter? I hope not!
        flat_outputs = compiled_fn(flat_inputs)
        return pytree.tree_unflatten(flat_outputs, jd.out_spec)

    return unflattened_compiled_fn

