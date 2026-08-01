
def _get_rnn_op_configs(dtype_configs: list[DTypeConfig]) -> list[BackendPatternConfig]:
    rnn_op_configs = []
    for rnn_op, ref_rnn_op in [
        (nn.GRUCell, nnqr.GRUCell),
        (nn.LSTMCell, nnqr.LSTMCell),
        (nn.RNNCell, nnqr.RNNCell),
        (nn.LSTM, nnqr.LSTM),
        (nn.GRU, nnqr.GRU),
    ]:
        rnn_op_configs.append(
            BackendPatternConfig(rnn_op)
            .set_observation_type(
                ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
            )  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(rnn_op)
            .set_reference_quantized_module(ref_rnn_op)
        )
    return rnn_op_configs

