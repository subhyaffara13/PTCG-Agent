from typing import Callable

def prune_lstm_output_linear(
    lstm: nn.LSTM, getitem: Callable, linear: nn.Linear
) -> None:
    prune_lstm_output_layernorm_linear(lstm, getitem, None, linear)

