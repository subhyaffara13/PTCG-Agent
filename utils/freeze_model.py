
def freeze_model(model, module_exceptions=()):
    mapping = {
        "LayerNorm": nn.LayerNorm,
        "Linear": nn.Linear,
        "Embedding": nn.Embedding,
    }
    module_exceptions_mapped = [mapping[m] for m in module_exceptions]
    for module in model.modules():
        if module_exceptions and any(isinstance(module, t) for t in module_exceptions_mapped):
            module.requires_grad_(True)  # Explicitly setting it to true to avoid any mistakes
        else:
            module.requires_grad_(False)
    return model

