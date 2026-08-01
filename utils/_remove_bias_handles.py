
def _remove_bias_handles(module: nn.Module) -> None:
    if hasattr(module, "_forward_hooks"):
        bias_hooks: list[int] = []
        for key, hook in module._forward_hooks.items():
            if isinstance(hook, BiasHook):
                bias_hooks.append(key)

        for key in bias_hooks:
            del module._forward_hooks[key]

