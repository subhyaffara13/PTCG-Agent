
def register_fusion(name: str, pre_grad=True):
    def decorator(fusion_cls: GroupBatchFusionBase):
        if pre_grad:
            PRE_GRAD_FUSIONS[name] = fusion_cls
        else:
            POST_GRAD_FUSIONS[name] = fusion_cls
        return fusion_cls

    return decorator

