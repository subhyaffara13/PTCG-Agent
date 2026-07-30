from . import np
from ._load_pickle_state_relu_tanh import linear, relu

class ActorCriticNumpy:
    """Pure-NumPy replica of ActorCritic (input_dim → 256 → 128 → logits/value)."""

    def __init__(self, state_dict: dict):
        self.base_w0 = state_dict["base.0.weight"]
        self.base_b0 = state_dict["base.0.bias"]
        self.base_ln_w0 = state_dict["base.2.weight"]
        self.base_ln_b0 = state_dict["base.2.bias"]
        self.base_w1 = state_dict["base.3.weight"]
        self.base_b1 = state_dict["base.3.bias"]
        self.base_ln_w1 = state_dict["base.5.weight"]
        self.base_ln_b1 = state_dict["base.5.bias"]
        self.actor_w = state_dict["actor.0.weight"]
        self.actor_b = state_dict["actor.0.bias"]
        self.critic_w = state_dict["critic.0.weight"]
        self.critic_b = state_dict["critic.0.bias"]

    @staticmethod
    def layer_norm(x, weight, bias, eps=1e-5):
        mean = x.mean(axis=-1, keepdims=True)
        var = x.var(axis=-1, keepdims=True)
        return weight * (x - mean) / np.sqrt(var + eps) + bias

    def forward(self, x: np.ndarray):
        x = linear(x, self.base_w0, self.base_b0)
        x = relu(x)
        x = self.layer_norm(x, self.base_ln_w0, self.base_ln_b0)
        x = linear(x, self.base_w1, self.base_b1)
        x = relu(x)
        x = self.layer_norm(x, self.base_ln_w1, self.base_ln_b1)
        logits = linear(x, self.actor_w, self.actor_b)
        value = linear(x, self.critic_w, self.critic_b)
        return logits, value

