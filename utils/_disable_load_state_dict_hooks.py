from typing import Callable

def _disable_load_state_dict_hooks(mod: torch.nn.Module):
    state_dict_hooks: dict[int, Callable] = dict(mod._state_dict_hooks)
    state_dict_pre_hooks: dict[int, Callable] = dict(mod._state_dict_pre_hooks)
    mod._state_dict_hooks.clear()
    mod._state_dict_pre_hooks.clear()
    try:
        yield
    finally:
        mod._state_dict_hooks = state_dict_hooks
        mod._state_dict_pre_hooks = state_dict_pre_hooks

