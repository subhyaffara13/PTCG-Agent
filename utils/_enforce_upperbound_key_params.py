
def _enforce_upperbound_key_params(
    data: Union[GenerateKeyRequest, UpdateKeyRequest],
    fill_defaults: bool = True,
) -> None:
    """
    Enforce upperbound limits on key parameters.

    For key generation (fill_defaults=True): fills None values with upperbound defaults.
    For key update (fill_defaults=False): only validates explicitly provided values.
    """
    # Always reject NaN / Inf regardless of whether an upperbound config is set
    # (GHSA-2rv4-xv66-fpjg): float('nan') passes every `< 0` check because
    # nan < 0 is False, and spend >= nan is always False, permanently disabling
    # budget enforcement for any key that carries it.
    for elem in data:
        key, value = elem
        if key in _BUDGET_NUMERIC_KEYS and value is not None:
            if not math.isfinite(value):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": f"{key} must be a finite number. Received: {value}"
                    },
                )

    if litellm.upperbound_key_generate_params is None:
        return

    for elem in data:
        key, value = elem
        upperbound_value = getattr(litellm.upperbound_key_generate_params, key, None)
        if upperbound_value is not None:
            if value is None:
                if fill_defaults:
                    setattr(data, key, upperbound_value)
            else:
                if key in [
                    "max_budget",
                    "max_parallel_requests",
                    "tpm_limit",
                    "rpm_limit",
                ]:
                    if value > upperbound_value:
                        raise HTTPException(
                            status_code=400,
                            detail={
                                "error": f"{key} is over max limit set in config - user_value={value}; max_value={upperbound_value}"
                            },
                        )
                elif key in ["budget_duration", "duration"]:
                    upperbound_duration = duration_in_seconds(duration=upperbound_value)
                    if value == "-1":
                        user_duration = float("inf")
                    else:
                        user_duration = duration_in_seconds(duration=value)
                    if user_duration > upperbound_duration:
                        raise HTTPException(
                            status_code=400,
                            detail={
                                "error": f"{key} is over max limit set in config - user_value={value}; max_value={upperbound_value}"
                            },
                        )

