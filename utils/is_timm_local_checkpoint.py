import json
import os

def is_timm_local_checkpoint(pretrained_model_path: str) -> bool:
    """
    Checks whether a checkpoint is a timm model checkpoint.
    """
    if pretrained_model_path is None:
        return False

    # in case it's Path, not str
    pretrained_model_path = str(pretrained_model_path)

    is_file = os.path.isfile(pretrained_model_path)
    is_dir = os.path.isdir(pretrained_model_path)

    # pretrained_model_path is a file
    if is_file and pretrained_model_path.endswith(".json"):
        with open(pretrained_model_path) as f:
            config_dict = json.load(f)
        return is_timm_config_dict(config_dict)

    # pretrained_model_path is a directory with a config.json
    if is_dir and os.path.exists(os.path.join(pretrained_model_path, "config.json")):
        with open(os.path.join(pretrained_model_path, "config.json")) as f:
            config_dict = json.load(f)
        return is_timm_config_dict(config_dict)

    return False

