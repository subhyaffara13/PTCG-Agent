
def _update_internal_user_params(
    data_json: dict, data: Union[UpdateUserRequest, UpdateUserRequestNoUserIDorEmail]
) -> dict:
    non_default_values = {}
    fields_set = data.fields_set() if hasattr(data, "fields_set") else set()

    for k, v in data_json.items():
        if k == "max_budget":
            if "max_budget" in fields_set:
                non_default_values[k] = v
        elif (
            v is not None
            and v
            not in (
                [],
                {},
            )
            and k not in LiteLLM_ManagementEndpoint_MetadataFields
        ):  # models default to [], spend defaults to 0, we should not reset these values
            non_default_values[k] = v

    is_internal_user = False
    if data.user_role == LitellmUserRoles.INTERNAL_USER:
        is_internal_user = True

    if "budget_duration" in non_default_values:
        from litellm.proxy.common_utils.timezone_utils import get_budget_reset_time

        non_default_values["budget_reset_at"] = get_budget_reset_time(
            budget_duration=non_default_values["budget_duration"]
        )

    if "max_budget" not in non_default_values:
        if (
            is_internal_user and litellm.max_internal_user_budget is not None
        ):  # applies internal user limits, if user role updated
            non_default_values["max_budget"] = litellm.max_internal_user_budget

    if (
        "budget_duration" not in non_default_values
    ):  # applies internal user limits, if user role updated
        if is_internal_user and litellm.internal_user_budget_duration is not None:
            non_default_values["budget_duration"] = (
                litellm.internal_user_budget_duration
            )
            from litellm.proxy.common_utils.timezone_utils import get_budget_reset_time

            non_default_values["budget_reset_at"] = get_budget_reset_time(
                budget_duration=non_default_values["budget_duration"]
            )

    return non_default_values

