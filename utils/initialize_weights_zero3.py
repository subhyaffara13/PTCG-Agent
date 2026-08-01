
def initialize_weights_zero3(model):
    """
    DeepSpeed ZeRO-3 variant of `PreTrainedModel.initialize_weights`. Mirrors the `smart_apply`
    dispatch logic but gathers each module's partitioned parameters before calling
    `_initialize_weights`, so initialization operates on full tensors instead of empty shards.
    Only rank 0 performs the actual init.
    """
    import deepspeed
    import torch

    from ..initialization import guard_torch_init_functions
    from ..modeling_utils import PreTrainedModel

    is_remote_code = model.is_remote_code()

    def _apply_zero3(model_or_module, fn):
        for child in model_or_module.children():
            if isinstance(child, PreTrainedModel):
                _apply_zero3(child, child._initialize_weights)
            else:
                _apply_zero3(child, fn)

        params = list(model_or_module.parameters(recurse=False))
        if params:
            with deepspeed.zero.GatheredParameters(params, modifier_rank=0):
                if deepspeed.comm.get_rank() == 0:
                    fn(model_or_module, is_remote_code)
        else:
            fn(model_or_module, is_remote_code)

    with torch.no_grad():
        with guard_torch_init_functions():
            _apply_zero3(model, model._initialize_weights)

