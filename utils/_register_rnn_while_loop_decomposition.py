
def _register_rnn_while_loop_decomposition(
    rnn_op, rnn_impl
) -> Generator[None, None, None]:
    """
    Generic context manager for registering while_loop-based RNN decompositions.

    Args:
        rnn_op: The aten operation to patch (e.g., torch.ops.aten.lstm.input)
        rnn_impl: The while_loop-based implementation function

    Note:
        This is an internal helper. Use register_lstm_while_loop_decomposition()
        or register_gru_while_loop_decomposition() instead.
    """
    registry = global_decomposition_table["post_autograd"]

    # Save the original decomposition if it exists
    original_decomp = registry.get(rnn_op, None)

    # Save the original py_kernel if it exists
    original_py_kernel = rnn_op.py_kernels.get(
        torch._C.DispatchKey.CompositeImplicitAutograd, None
    )

    try:
        # Register our while_loop-based implementation
        registry[rnn_op] = rnn_impl
        rnn_op.py_kernels[torch._C.DispatchKey.CompositeImplicitAutograd] = rnn_impl
        yield
    finally:
        # Restore the original decomposition
        if original_decomp is not None:
            registry[rnn_op] = original_decomp
        else:
            # If there was no original, remove our registration
            registry.pop(rnn_op, None)

        # Restore the original py_kernel
        if original_py_kernel is not None:
            rnn_op.py_kernels[torch._C.DispatchKey.CompositeImplicitAutograd] = (
                original_py_kernel
            )
        else:
            # If there was no original, remove our registration
            rnn_op.py_kernels.pop(torch._C.DispatchKey.CompositeImplicitAutograd, None)

