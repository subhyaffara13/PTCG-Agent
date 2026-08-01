
def get_cudnn_mode(mode):
    if mode == "RNN_RELU":
        # pyrefly: ignore [missing-attribute]
        return int(_cudnn.RNNMode.rnn_relu)
    elif mode == "RNN_TANH":
        # pyrefly: ignore [missing-attribute]
        return int(_cudnn.RNNMode.rnn_tanh)
    elif mode == "LSTM":
        # pyrefly: ignore [missing-attribute]
        return int(_cudnn.RNNMode.lstm)
    elif mode == "GRU":
        # pyrefly: ignore [missing-attribute]
        return int(_cudnn.RNNMode.gru)
    else:
        raise ValueError(f"Unknown mode: {mode}")  # noqa: TRY002

