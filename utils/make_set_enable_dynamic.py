from typing import Any

def make_set_enable_dynamic(enable: bool) -> Any:
    assert isinstance(enable, bool)
    if enable:
        # Assume everything is dynamic by default
        return config._make_closure_patcher(assume_static_by_default=False)
    else:
        return config._make_closure_patcher(
            automatic_dynamic_shapes=False, assume_static_by_default=True
        )

