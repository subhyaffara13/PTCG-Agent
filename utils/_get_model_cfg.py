
def _get_model_cfg(model_type) -> str:
    assert model_type in ["sam2_hiera_tiny", "sam2_hiera_small", "sam2_hiera_large", "sam2_hiera_base_plus"]
    if model_type == "sam2_hiera_tiny":
        model_cfg = "sam2_hiera_t.yaml"
    elif model_type == "sam2_hiera_small":
        model_cfg = "sam2_hiera_s.yaml"
    elif model_type == "sam2_hiera_base_plus":
        model_cfg = "sam2_hiera_b+.yaml"
    else:
        model_cfg = "sam2_hiera_l.yaml"
    return model_cfg

