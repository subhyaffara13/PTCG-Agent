
def tag_activation_checkpoint_impl(gmod, *args, **kwargs):
    import functools

    import torch.fx.traceback as fx_traceback
    from torch.fx import Interpreter
    from torch.utils.checkpoint import create_selective_checkpoint_contexts

    unique_graph_id = next(uid)
    if "_checkpoint_context_fn" in gmod.meta:
        context_fn = gmod.meta["_checkpoint_context_fn"]
        warning_once(
            log,
            """
Detected that context_fn is passed to torch.utils.checkpoint under torch.compile.
Please make sure the checkpointed region does not contain in-place ops (e.g. torch.relu_).
""",
        )
    else:
        # Vanilla AC: use the SAC path with a policy that always recomputes.
        context_fn = functools.partial(
            create_selective_checkpoint_contexts, _always_prefer_recompute
        )

    def context_fn_with_graph_id():
        fwd_ctx, recomp_ctx = context_fn()
        # Plumb ac_graph_id so _CachingTorchDispatchMode tags all nodes
        # (including ops from desugared HOPs like custom autograd.Function).
        fwd_ctx.ac_graph_id = unique_graph_id
        return fwd_ctx, recomp_ctx

    # use_reentrant is set to False because this op is going to be traced.
    # And we ensure that AOT Autograd traces through the non reentrant
    # version of checkpointing.
    kwargs["use_reentrant"] = False
    # preserve_rng_state is set to False because we want to prevent AOTAutograd from tracing through
    # `torch.random.fork_rng` op (which is not supported yet under CUDA).
    # This doesn't mean that we don't preserve RNG state. Instead, we will always preserve RNG state
    # regardless of this flag (by doing RNG functionalization via `replace_random_passes` in Inductor
    # instead of in AOTAutograd).
    kwargs["preserve_rng_state"] = False
    kwargs["context_fn"] = context_fn_with_graph_id
    # Disable early stop to prevent _StopRecomputationError from interrupting
    # recomputation between _vmap_increment_nesting and _vmap_decrement_nesting,
    # which would leak a functorch dynamic layer.
    kwargs["early_stop"] = False
    # Using interpreter allows preservation of metadata through torch.compile stack.
    # We use a wrapper instead of passing Interpreter(gmod).run directly because
    # checkpoint's recompute_fn captures the function in a closure. A bound method
    # reference would keep the Interpreter alive, whose env dict retains the output
    # tensors and prevents the autograd graph from being freed.

    def run_with_interpreter(*args):
        return Interpreter(gmod).run(*args)

    with fx_traceback.preserve_node_meta():
        from torch.utils.checkpoint import checkpoint

        return checkpoint(run_with_interpreter, *args, **kwargs)

