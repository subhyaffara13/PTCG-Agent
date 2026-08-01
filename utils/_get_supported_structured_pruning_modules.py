
def _get_supported_structured_pruning_modules():
    SUPPORTED_STRUCTURED_PRUNING_MODULES = {  # added to config if None given
        nn.Linear,
        nn.Conv2d,
        nn.LSTM,
    }
    return SUPPORTED_STRUCTURED_PRUNING_MODULES

