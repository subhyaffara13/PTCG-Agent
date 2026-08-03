import itertools
import random

def reset() -> None:
    """
    This function clears all compilation caches and restores the system to its initial state.
    It is recommended to call this function, especially after using operations like `torch.compile(...)`
    to ensure a clean state before another unrelated compilation
    """
    import torch._dynamo

    torch._dynamo.reset()


def reset() -> None:
    global compiled_autograd_enabled
    compiled_autograd_enabled = False
    assert not in_compiled_autograd_region
    torch._C._dynamo.compiled_autograd.set_autograd_compiler(None, False)
    torch._C._dynamo.compiled_autograd.set_verbose_logger(None)
    torch._C._dynamo.compiled_autograd.clear_cache()
    global COMPILE_COUNTER
    COMPILE_COUNTER = itertools.count()


def reset() -> None:
    """
    Clear all compile caches and restore initial state.  This function is intended
    to reset Dynamo's state *as if* you had started a fresh process invocation, which
    makes it good for testing scenarios where you want to behave as if you started
    a new process.  It does NOT affect any file system caches.

    NB: this does NOT reset logging state.  Don't use this to test logging
    initialization/reinitialization.
    """
    # TODO: https://github.com/pytorch/pytorch/issues/139200
    import logging

    log = logging.getLogger(__name__)
    log.info("torch._dynamo.reset")
    with convert_frame.compile_lock:
        reset_code_caches()
        convert_frame.input_codes.clear()
        reset_code_state()
        convert_frame.output_codes.clear()
        orig_code_map.clear()
        guard_failures.clear()
        graph_break_reasons.clear()
        resume_execution.ContinueExecutionCache.cache.clear()
        _reset_guarded_backend_cache()
        reset_frame_count()
        torch._dynamo.compiled_autograd.reset()
        convert_frame.FRAME_COUNTER = 0
        convert_frame.FRAME_COMPILE_COUNTER.clear()
        callback_handler.clear()
        GenerationTracker.clear()
        TensorifyState.clear()
        torch._dynamo.utils.warn_once_cache.clear()
        torch._C._autograd._saved_tensors_hooks_set_tracing(False)

        # Reset cudagraph trees unconditionally since they are global state
        # not tied to a specific backend instance
        from torch._higher_order_ops.triton_kernel_wrap import kernel_side_table
        from torch._higher_order_ops.wrap import inductor_code_side_table

        kernel_side_table.reset_table()
        inductor_code_side_table.reset_table()

        if torch.cuda.is_available():
            from torch._inductor.cudagraph_trees import reset_cudagraph_trees

            reset_cudagraph_trees()


def reset() -> None:
    global generated_kernel_count
    global generated_cpp_vec_kernel_count
    global num_bytes_accessed, nodes_num_elem
    global ir_nodes_pre_fusion
    global cpp_to_dtype_count
    global cpp_outer_loop_fused_inner_counts
    global num_comprehensive_padding
    global num_matches_for_scatter_upon_const_tensor
    global num_loop_reordering
    global parallel_reduction_count
    global codegen_mix_order_reduction
    global num_auto_chunking

    generated_kernel_count = 0
    generated_cpp_vec_kernel_count = 0
    num_bytes_accessed = 0
    nodes_num_elem.clear()
    node_runtimes.clear()
    ir_nodes_pre_fusion = 0
    cpp_to_dtype_count = 0
    cpp_outer_loop_fused_inner_counts.clear()
    num_comprehensive_padding = 0
    num_matches_for_scatter_upon_const_tensor = 0
    num_loop_reordering = 0
    parallel_reduction_count = 0
    codegen_mix_order_reduction = 0
    num_auto_chunking = 0


def reset():
    """Clear TrieCache. This is needed in testing to avoid
    node reusing between different tests.
    """
    return torch._C._lazy._clear_ir_cache()


def reset():
    """Resets all metric counters."""
    torch._C._lazy._reset_metrics()


def reset():
    global balls
    global target_position

    target_position = None
    balls = []
    for x in range(MAX_BALLS):
        pos = pg.Vector2(
            random.randint(0, int(SCREEN_SIZE.x)), random.randint(0, int(SCREEN_SIZE.y))
        )
        speed = random.uniform(MIN_SPEED, MAX_SPEED)

        b = Ball(pos, speed)
        balls.append(b)

