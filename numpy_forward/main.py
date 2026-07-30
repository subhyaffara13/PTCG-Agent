from . import Path, np
from .actorcriticnumpy import ActorCriticNumpy
from .load_pth import load_pth
from .ptcgvaluemlpnumpy import PTCGValueMLPNumpy
from .state_to_tensor import state_to_tensor

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

