import os
import sys

def load_sam2_model(sam2_dir, model_type, device: str | torch.device = "cpu") -> SAM2Base:
    checkpoints_dir = os.path.join(sam2_dir, "checkpoints")
    sam2_config_dir = os.path.join(sam2_dir, "sam2_configs")
    if not os.path.exists(sam2_dir):
        raise FileNotFoundError(f"{sam2_dir} does not exist. Please specify --sam2_dir correctly.")

    if not os.path.exists(checkpoints_dir):
        raise FileNotFoundError(f"{checkpoints_dir} does not exist. Please specify --sam2_dir correctly.")

    if not os.path.exists(sam2_config_dir):
        raise FileNotFoundError(f"{sam2_config_dir} does not exist. Please specify --sam2_dir correctly.")

    checkpoint_path = os.path.join(checkpoints_dir, f"{model_type}.pt")
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"{checkpoint_path} does not exist. Please download checkpoints under the directory.")

    if sam2_dir not in sys.path:
        sys.path.append(sam2_dir)

    model_cfg = _get_model_cfg(model_type)
    sam2_model = build_sam2(model_cfg, checkpoint_path, device=device)
    return sam2_model

