
def _get_backbone_hidden_size(config):
    if config.backbone_config is not None and hasattr(config.backbone_config, "hidden_size"):
        return config.backbone_config.hidden_size
    else:
        return config.hidden_size


def _get_backbone_hidden_size(config):
    if config.backbone_config is not None and hasattr(config.backbone_config, "hidden_size"):
        return config.backbone_config.hidden_size
    else:
        return config.hidden_size

