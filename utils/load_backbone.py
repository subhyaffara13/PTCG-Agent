
def load_backbone(config):
    """
    Loads the backbone model from a config object.

    If the config is from the backbone model itself, then we return a backbone model with randomly initialized
    weights.

    If the config is from the parent model of the backbone model itself, then we load the pretrained backbone weights
    if specified.
    """
    from transformers import AutoBackbone

    backbone_config = getattr(config, "backbone_config", None)

    if backbone_config is None:
        backbone = AutoBackbone.from_config(config=config)
    else:
        backbone = AutoBackbone.from_config(config=backbone_config)
    return backbone

