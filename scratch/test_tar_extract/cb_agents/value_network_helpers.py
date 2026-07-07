"""
cb_agents/value_network_helpers.py
Defines the PyTorch MLP Value Network architecture for CPU-only training/evals.
Falls back to a pure-NumPy forward pass on Kaggle to avoid importing PyTorch.
"""
import os
import numpy as np

is_kaggle = any(k.startswith("KAGGLE") for k in os.environ) or not os.path.exists("build_submission.py")

if is_kaggle:
    import zipfile, pickle, io, collections
    from pathlib import Path

    class NumpyTensorMock:
        def __init__(self, val):
            self.val = val
        def item(self) -> float:
            return float(self.val)
        def __float__(self):
            return float(self.val)

    class PTCGValueMLP:
        """Pure-NumPy replica of PTCGValueMLP (20 -> 64 -> 32 -> 1 + Tanh)."""
        def __init__(self, input_dim=20):
            self.w0 = np.zeros((1, 1))
            self.b0 = np.zeros(1)
            self.w1 = np.zeros((1, 1))
            self.b1 = np.zeros(1)
            self.w2 = np.zeros((1, 1))
            self.b2 = np.zeros(1)

        def load_state_dict(self, state_dict: dict):
            self.w0 = state_dict["model.0.weight"]   # [64, 20]
            self.b0 = state_dict["model.0.bias"]     # [64]
            self.w1 = state_dict["model.2.weight"]   # [32, 64]
            self.b1 = state_dict["model.2.bias"]     # [32]
            self.w2 = state_dict["model.4.weight"]   # [1, 32]
            self.b2 = state_dict["model.4.bias"]     # [1]

        def eval(self):
            pass

        def __call__(self, x: np.ndarray) -> NumpyTensorMock:
            # Forward pass
            x = x @ self.w0.T + self.b0
            x = np.maximum(0, x)  # ReLU
            x = x @ self.w1.T + self.b1
            x = np.maximum(0, x)  # ReLU
            x = x @ self.w2.T + self.b2
            x = np.tanh(x)        # Tanh
            return NumpyTensorMock(x.item())

    def load_weights(path):
        """Load PyTorch checkpoint without importing torch."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"{path} not found")
        raw = path.read_bytes()
        if raw[:2] == b"PK":
            return _load_zip_state(path)
        return _load_pickle_state(raw)

    def _load_zip_state(path):
        with zipfile.ZipFile(path) as z:
            namelist = z.namelist()
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
                    raise pickle.UnpicklingError(f"Unknown: {module}.{name}")

                def _UntypedStorage(self, *args, **kwargs):
                    sz = args[0] if args else 0
                    return np.zeros(sz, dtype=np.uint8)

                def _FloatStorage(self, *args, **kwargs):
                    return None

                def _rebuild_tensor_v2(self, storage, storage_offset, size, stride, requires_grad, backward_hooks):
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

            def _rebuild_tensor_v2(self, storage, storage_offset, size, stride, requires_grad, backward_hooks):
                if isinstance(storage, np.ndarray):
                    raw = np.frombuffer(storage.tobytes(), dtype=np.float32)
                    return raw[storage_offset:].reshape(size)
                return np.zeros(size, dtype=np.float32)

            def _rebuild_parameter(self, *args, **kwargs):
                return args[0] if args else None

        return _Unpickler(io.BytesIO(raw)).load()

    def state_to_tensor(game_state: dict) -> np.ndarray:
        """Convert game state dict -> 20-element float32 feature vector for NumPy."""
        my_prizes = float(game_state.get("my_prizes", 6)) / 6.0
        opp_prizes = float(game_state.get("opponent_prizes", 6)) / 6.0
        my_active_hp = game_state.get("my_active_hp", 100) / 100.0
        opp_active_hp = game_state.get("opponent_active_hp", 100) / 100.0

        active = game_state.get("my_active_pokemon", {}) or {}
        attached = float(len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0) / 10.0

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

        return np.array(features, dtype=np.float32).reshape(1, -1)

else:
    try:
        import torch
        import torch.nn as nn

        class PTCGValueMLP(nn.Module):
            def __init__(self, input_dim=20):
                super().__init__()
                self.model = nn.Sequential(
                    nn.Linear(input_dim, 64),
                    nn.ReLU(),
                    nn.Linear(64, 32),
                    nn.ReLU(),
                    nn.Linear(32, 1),
                    nn.Tanh()
                )
                
            def forward(self, x):
                return self.model(x)
                
        def load_weights(path):
            return torch.load(str(path), map_location="cpu")

        def state_to_tensor(game_state: dict) -> torch.Tensor:
            """Converts game state dictionary to a numeric tensor for the MLP."""
            my_prizes = game_state.get("my_prizes", 6)
            opp_prizes = game_state.get("opponent_prizes", 6)
            my_active_hp = game_state.get("my_active_hp", 100) / 100.0
            opp_active_hp = game_state.get("opponent_active_hp", 100) / 100.0
            
            active = game_state.get("my_active_pokemon", {}) or {}
            attached = len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0
            
            my_bench = game_state.get("my_bench", [])
            opp_bench = game_state.get("opponent_bench", [])
            my_bench_size = len(my_bench) if isinstance(my_bench, list) else 0
            opp_bench_size = len(opp_bench) if isinstance(opp_bench, list) else 0
            
            my_hand = game_state.get("my_hand", [])
            my_hand_size = len(my_hand) if isinstance(my_hand, list) else 0
            
            turn = game_state.get("turn_number", 0)
            
            my_discard = game_state.get("my_discard_pile", [])
            opp_discard = game_state.get("opponent_discard_pile", [])
            my_discard_size = len(my_discard) if isinstance(my_discard, list) else 0
            opp_discard_size = len(opp_discard) if isinstance(opp_discard, list) else 0
            
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
                float(my_prizes) / 6.0, 
                float(opp_prizes) / 6.0, 
                float(my_active_hp), 
                float(opp_active_hp), 
                float(attached) / 10.0,
                float(my_bench_size) / 5.0,
                float(opp_bench_size) / 5.0,
                float(my_hand_size) / 10.0,
                float(turn) / 20.0,
                float(my_discard_size) / 60.0,
                float(opp_discard_size) / 60.0,
                stadium,
                weakness_mult,
                resistance_mult
            ] + [0.0]*6
            
            return torch.tensor(features, dtype=torch.float32).unsqueeze(0)
    except ImportError:
        class PTCGValueMLP:
            def __init__(self, input_dim=20): pass
            def load_state_dict(self, state_dict: dict): pass
            def eval(self): pass
            def __call__(self, x): pass
        def state_to_tensor(game_state: dict):
            return None
        def load_weights(path):
            raise NotImplementedError("PyTorch is not available.")
