
def _has_special_act_post_process(module: torch.nn.Module) -> bool:
    return module.training and type(module) in DEFAULT_MODULE_TO_ACT_POST_PROCESS

