
def register_lstm_while_loop_decomposition() -> Generator[None, None, None]:
    """
    Context manager that temporarily registers the while_loop-based LSTM decomposition.

    The while_loop-based decomposition is more suitable for export and graph-based
    execution, as it avoids Python control flow that cannot be captured in the graph.
    This should support dynamic sequence lengths, however as while_loop does not
    support Autograd yet, an ExportedProgram created with this will not be trainable.

    Usage::

        from torch.export._patches import register_lstm_while_loop_decomposition
        from torch.export import export

        with register_lstm_while_loop_decomposition():
            # Export your model with LSTM
            ep = export(model, (x, h0, c0))

    Note:
        This context manager temporarily modifies the global decomposition table
        and py_kernels registration. The original registrations are restored when
        exiting the context.
    """
    with _register_rnn_while_loop_decomposition(
        torch.ops.aten.lstm.input, lstm_while_loop_impl
    ):
        yield

