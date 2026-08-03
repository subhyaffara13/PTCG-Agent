from typing import Optional

def _pop_and_merge_extra_body(data: RequestBody, optional_params: dict) -> None:
    """Pop extra_body from optional_params and shallow-merge into data, deep-merging dict values."""
    extra_body: Optional[dict] = optional_params.pop("extra_body", None)
    if extra_body is not None:
        data_dict: dict = data  # type: ignore[assignment]
        for k, v in extra_body.items():
            if k in _LITELLM_INTERNAL_EXTRA_BODY_KEYS:
                continue
            if (
                k in data_dict
                and isinstance(data_dict[k], dict)
                and isinstance(v, dict)
            ):
                data_dict[k].update(v)
            else:
                data_dict[k] = v

