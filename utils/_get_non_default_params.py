from typing import Optional

def _get_non_default_params(
    passed_params: dict, default_params: dict, additional_drop_params: Optional[list]
) -> dict:
    non_default_params = {}
    for k, v in passed_params.items():
        if (
            k in default_params
            and v != default_params[k]
            and _should_drop_param(k=k, additional_drop_params=additional_drop_params)
            is False
        ):
            non_default_params[k] = v

    return non_default_params

