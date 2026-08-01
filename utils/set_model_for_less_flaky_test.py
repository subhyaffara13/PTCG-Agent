
def set_model_for_less_flaky_test(model):
    # Another way to make sure norm layers have desired epsilon. (Some models don't set it from its config.)
    target_names = (
        "LayerNorm",
        "GroupNorm",
        "BatchNorm",
        "RMSNorm",
        "BatchNorm2d",
        "BatchNorm1d",
        "BitGroupNormActivation",
        "WeightStandardizedConv2d",
    )
    target_attrs = ["eps", "epsilon", "variance_epsilon"]
    if is_torch_available() and isinstance(model, torch.nn.Module):
        for module in model.modules():
            if type(module).__name__.endswith(target_names):
                for attr in target_attrs:
                    if hasattr(module, attr):
                        setattr(module, attr, 1.0)

