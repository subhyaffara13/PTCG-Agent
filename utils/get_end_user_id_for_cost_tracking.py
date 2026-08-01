
def get_end_user_id_for_cost_tracking(
    litellm_params: dict,
    service_type: Literal["litellm_logging", "prometheus"] = "litellm_logging",
) -> Optional[str]:
    """
    Used for enforcing `disable_end_user_cost_tracking` param.

    service_type: "litellm_logging" or "prometheus" - used to allow prometheus only disable cost tracking.
    """
    get_litellm_metadata_from_kwargs = getattr(
        sys.modules[__name__], "get_litellm_metadata_from_kwargs"
    )
    _metadata = cast(
        dict, get_litellm_metadata_from_kwargs(dict(litellm_params=litellm_params))
    )

    end_user_id = cast(
        Optional[str],
        litellm_params.get("user_api_key_end_user_id")
        or _metadata.get("user_api_key_end_user_id"),
    )
    if litellm.disable_end_user_cost_tracking:
        return None

    #######################################
    # By default we don't track end_user on prometheus since we don't want to increase cardinality
    # by default litellm.enable_end_user_cost_tracking_prometheus_only is None, so we don't track end_user on prometheus
    #######################################
    if service_type == "prometheus":
        if litellm.enable_end_user_cost_tracking_prometheus_only is not True:
            return None
    return end_user_id

