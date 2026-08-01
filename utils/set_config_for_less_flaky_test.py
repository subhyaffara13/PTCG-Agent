
def set_config_for_less_flaky_test(config):
    target_attrs = [
        "rms_norm_eps",
        "layer_norm_eps",
        "norm_eps",
        "norm_epsilon",
        "layer_norm_epsilon",
        "batch_norm_eps",
    ]
    for target_attr in target_attrs:
        setattr(config, target_attr, 1.0)

    # norm layers (layer/group norm, etc.) could cause flaky tests when the tensors have very small variance.
    # (We don't need the original epsilon values to check eager/sdpa matches)
    attrs = ["text_config", "vision_config", "audio_config", "text_encoder", "audio_encoder", "decoder"]
    for attr in attrs:
        if hasattr(config, attr) and getattr(config, attr) is not None:
            for target_attr in target_attrs:
                setattr(getattr(config, attr), target_attr, 1.0)

