import torch
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.getcwd())

from factory.ppo_trainer_network import ActorCritic
from factory.state_dimensions import STATE_DIM

def main():
    model_path = "models/ppo_actor_critic.pt"
    onnx_path = "models/ppo_actor_critic.onnx"
    
    print(f"Loading PyTorch model from {model_path}...")
    import typing
    model: typing.Any = ActorCritic(input_dim=STATE_DIM, hidden_dim=256, action_dim=3000)
    model.load_state_dict(torch.load(model_path, map_location="cpu", weights_only=True))
    model.eval()
    
    # Create dummy inputs matching the forward signature
    dummy_token_ids = torch.zeros(1, 32, dtype=torch.long)
    dummy_zone_ids = torch.zeros(1, 32, dtype=torch.long)
    dummy_scalars = torch.zeros(1, 6, dtype=torch.float32)
    dummy_padding_mask = torch.zeros(1, 33, dtype=torch.bool)
    
    print("Exporting model to ONNX...")
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        torch.onnx.export(
            model,
            (None, dummy_token_ids, dummy_zone_ids, dummy_scalars, dummy_padding_mask),
            onnx_path,
            input_names=["x", "token_ids", "zone_ids", "scalars", "padding_mask"],
            output_names=["logits", "value"],
            dynamic_axes={
                "token_ids": {0: "batch_size"},
                "zone_ids": {0: "batch_size"},
                "scalars": {0: "batch_size"},
                "padding_mask": {0: "batch_size"},
                "logits": {0: "batch_size"},
                "value": {0: "batch_size"}
            },
            opset_version=14
        )
    print(f"ONNX model successfully exported to {onnx_path}")

if __name__ == "__main__":
    main()
