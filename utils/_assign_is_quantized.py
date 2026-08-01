
def _assign_is_quantized(model):
    from ..modeling_utils import PreTrainedModel

    for module in model.modules():
        if isinstance(module, PreTrainedModel):
            module.config._is_quantized = True

