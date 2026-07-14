"""
Lightweight pure-NumPy forward pass for PTCGValueMLP.
Loads PyTorch .pth/.pt checkpoints without importing torch.

Usage:
    python numpy_forward.py                          # try logs/model_weights.pth
    python numpy_forward.py path/to/model_weights.pth # custom path
"""

import zipfile, pickle, io, collections
from pathlib import Path
import numpy as np

# ── PyTorch-checkpoint loader (pure Python + NumPy) ──────────────────────

def load_pth(path):
    """Load a PyTorch state_dict from a .pth/.pt file into numpy arrays.
    Handles both zip-based (PyTorch >=1.6) and old pickle formats.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    raw = path.read_bytes()

    # zip-based format  (PyTorch >= 1.6)
    if raw[:2] == b"PK":
        return _load_zip_state(path)

    # old pickle format (fallback)
    return _load_pickle_state(raw)


def _load_zip_state(path):
    """Load state_dict from zip-archive .pt file."""
    with zipfile.ZipFile(path) as z:
        namelist = z.namelist()

        # Determine archive prefix (e.g. 'm71/' or 'ppo_actor_critic/')
        prefixes = {n.split("/")[0] for n in namelist if "/" in n}
        prefix = next(iter(prefixes)) if prefixes else ""

        pkl_data = z.read(f"{prefix}/data.pkl") if prefix else z.read("data.pkl")

        class _Unpickler(pickle.Unpickler):
            def __init__(self, *a, zf=None, zprefix="", **kw):
                super().__init__(*a, **kw)
                self.zf = zf
                self.zprefix = zprefix

            def find_class(self, module, name):
                if module == "collections" and name == "OrderedDict":
                    return collections.OrderedDict
                if module == "torch._utils":
                    if name == "_rebuild_tensor_v2":
                        return self._rebuild_tensor_v2
                    if name == "_rebuild_parameter":
                        return self._rebuild_parameter
                if module == "torch.storage" and name == "_UntypedStorage":
                    return self._UntypedStorage
                if module == "torch" and name == "FloatStorage":
                    return self._FloatStorage
                if module == "torch" and name == "Size":
                    return tuple
                if module == "builtins":
                    b = __builtins__
                    return b[name] if isinstance(b, dict) else getattr(b, name)
                raise pickle.UnpicklingError(f"Unknown module/name: {module}.{name}")

            def _UntypedStorage(self, *args, **kwargs):
                sz = args[0] if args else 0
                return np.zeros(sz, dtype=np.uint8)

            def _FloatStorage(self, *args, **kwargs):
                return None

            def _rebuild_tensor_v2(self, storage, storage_offset, size,
                                    stride, requires_grad, backward_hooks):
                if isinstance(storage, np.ndarray):
                    raw = np.frombuffer(storage.tobytes(), dtype=np.float32)
                    return raw[storage_offset:].reshape(size)
                return np.zeros(size, dtype=np.float32)

            def _rebuild_parameter(self, *args, **kwargs):
                return args[0] if args else None

            def persistent_load(self, pid):
                if isinstance(pid, tuple) and len(pid) >= 4 and pid[0] == "storage":
                    _fn, _storage_type_fn, data_id, _device, numel = pid
                    if self.zf and self.zprefix:
                        inzip = f"{self.zprefix}/data/{data_id}"
                        if inzip in self.zf.namelist():
                            raw_bytes = self.zf.read(inzip)
                            return np.frombuffer(raw_bytes, dtype=np.uint8)
                return None

        u = _Unpickler(io.BytesIO(pkl_data), zf=z, zprefix=prefix)
        return u.load()


def _load_pickle_state(raw):
    """Load state_dict from old-format pickled checkpoint."""
    class _Unpickler(pickle.Unpickler):
        def find_class(self, module, name):
            if module == "collections" and name == "OrderedDict":
                return collections.OrderedDict
            if module == "torch._utils":
                if name == "_rebuild_tensor_v2":
                    return self._rebuild_tensor_v2
                if name == "_rebuild_parameter":
                    return self._rebuild_parameter
            if module in ("torch", "torch.storage"):
                if name in ("FloatStorage", "_UntypedStorage"):
                    return self._UntypedStorage
            if module == "torch" and name == "Size":
                return tuple
            if module == "builtins":
                b = __builtins__
                return b[name] if isinstance(b, dict) else getattr(b, name)
            raise pickle.UnpicklingError(f"Unknown {module}.{name}")

        def _UntypedStorage(self, *args, **kwargs):
            sz = args[0] if args else 0
            return np.zeros(sz, dtype=np.uint8)

        def _rebuild_tensor_v2(self, storage, storage_offset, size,
                                stride, requires_grad, backward_hooks):
            if isinstance(storage, np.ndarray):
                raw = np.frombuffer(storage.tobytes(), dtype=np.float32)
                return raw[storage_offset:].reshape(size)
            return np.zeros(size, dtype=np.float32)

        def _rebuild_parameter(self, *args, **kwargs):
            return args[0] if args else None

    return _Unpickler(io.BytesIO(raw)).load()


# ── MLP forward pass ─────────────────────────────────────────────────────

def relu(x):
    return np.maximum(0, x)


def tanh(x):
    return np.tanh(x)


def linear(x, weight, bias):
    return x @ weight.T + bias


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


# ── State → feature vector (14 handcrafted + 6 zero padding = 20) ───────

def state_to_tensor(game_state: dict) -> np.ndarray:
    """Convert game state dict → 20-element float32 feature vector."""
    my_prizes = float(game_state.get("my_prizes", 6)) / 6.0
    opp_prizes = float(game_state.get("opponent_prizes", 6)) / 6.0
    my_active_hp = game_state.get("my_active_hp", 100) / 100.0
    opp_active_hp = game_state.get("opponent_active_hp", 100) / 100.0

    active = game_state.get("my_active_pokemon", {}) or {}
    attached = float(len(active.get("attached", []) or active.get("energies", []))) / 10.0

    my_bench = game_state.get("my_bench", [])
    opp_bench = game_state.get("opponent_bench", [])
    my_bench_size = float(len(my_bench) if isinstance(my_bench, list) else 0) / 5.0
    opp_bench_size = float(len(opp_bench) if isinstance(opp_bench, list) else 0) / 5.0

    my_hand = game_state.get("my_hand", [])
    my_hand_size = float(len(my_hand) if isinstance(my_hand, list) else 0) / 10.0

    turn = float(game_state.get("turn_number", 0)) / 20.0

    my_discard = game_state.get("my_discard_pile", [])
    opp_discard = game_state.get("opponent_discard_pile", [])
    my_discard_size = float(len(my_discard) if isinstance(my_discard, list) else 0) / 60.0
    opp_discard_size = float(len(opp_discard) if isinstance(opp_discard, list) else 0) / 60.0

    stadium = 1.0 if game_state.get("stadium_card") else 0.0

    weakness_mult = 0.0
    resistance_mult = 0.0
    opp_active = game_state.get("opponent_active_pokemon", {}) or {}
    if isinstance(active, dict) and isinstance(opp_active, dict):
        my_type = active.get("element_type", "")
        opp_weakness = opp_active.get("weakness", "")
        opp_resistance = opp_active.get("resistance", "")
        if my_type and opp_weakness and my_type.lower() == opp_weakness.lower():
            weakness_mult = 1.0
        if my_type and opp_resistance and my_type.lower() == opp_resistance.lower():
            resistance_mult = 1.0

    features = [
        my_prizes, opp_prizes, my_active_hp, opp_active_hp, attached,
        my_bench_size, opp_bench_size, my_hand_size, turn,
        my_discard_size, opp_discard_size, stadium,
        weakness_mult, resistance_mult,
    ] + [0.0] * 6

    return np.array(features, dtype=np.float32)


# ── CLI entry point ──────────────────────────────────────────────────────

def main():
    import sys, json

    path = sys.argv[1] if len(sys.argv) > 1 else "logs/model_weights.pth"
    print(f"[numpy_forward] Loading: {path}")

    try:
        state_dict = load_pth(path)
    except FileNotFoundError:
        print(f"[numpy_forward] ERROR: {path} not found.")
        print("  Provide a path or place model_weights.pth in logs/")
        sys.exit(1)

    print(f"[numpy_forward] Loaded {len(state_dict)} keys:")
    for k, v in state_dict.items():
        print(f"    {k}: {v.shape}  dtype={v.dtype}  "
              f"range=[{v.min():.4f}, {v.max():.4f}]")

    # Auto-detect architecture from key names
    if "model.0.weight" in state_dict:
        model = PTCGValueMLPNumpy(state_dict)
        model_type = "PTCGValueMLP"
    elif "base.0.weight" in state_dict:
        model = ActorCriticNumpy(state_dict)
        model_type = "ActorCritic"
    else:
        print("[numpy_forward] Unknown architecture – keys:",
              list(state_dict.keys()))
        sys.exit(1)

    print(f"[numpy_forward] Architecture: {model_type}")
    input_dim = state_dict[list(state_dict.keys())[0]].shape[1]
    print(f"[numpy_forward] Input dim: {input_dim}")

    # Demo forward pass with dummy input
    dummy_x = np.random.randn(1, input_dim).astype(np.float32)
    if model_type == "PTCGValueMLP":
        output = model.forward(dummy_x)
        print(f"\n  Dummy input -> value: {output:.6f}")
    else:
        logits, value = model.forward(dummy_x)
        print(f"\n  Dummy input -> value: {value.item():.6f}, "
              f"logits shape: {logits.shape}")

    # Try demo with state_to_tensor if game state provided
    state_file = Path("logs/latest_state.json")
    if state_file.exists():
        with open(state_file) as f:
            game_state = json.load(f)
        x = state_to_tensor(game_state)
        if model_type == "PTCGValueMLP":
            val = model.forward(x.reshape(1, -1))
            print(f"\n  Real game state -> value: {val:.6f}")
        else:
            print(f"\n  Real game state shape: {x.shape}")


if __name__ == "__main__":
    main()
