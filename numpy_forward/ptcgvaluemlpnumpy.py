from . import np
from ._load_pickle_state_relu_tanh import linear, relu, tanh

class PTCGValueMLPNumpy:
    """Pure-NumPy replica of PTCGValueMLP (20 → 64 → 32 → 1 + Tanh)."""

    def __init__(self, state_dict: dict):
        self.w0 = state_dict["model.0.weight"]   # [64, 20]
        self.b0 = state_dict["model.0.bias"]     # [64]
        self.w1 = state_dict["model.2.weight"]   # [32, 64]
        self.b1 = state_dict["model.2.bias"]     # [32]
        self.w2 = state_dict["model.4.weight"]   # [1, 32]
        self.b2 = state_dict["model.4.bias"]     # [1]

    def forward(self, x: np.ndarray) -> float:
        x = linear(x, self.w0, self.b0)
        x = relu(x)
        x = linear(x, self.w1, self.b1)
        x = relu(x)
        x = linear(x, self.w2, self.b2)
        x = tanh(x)
        return float(x.item())

