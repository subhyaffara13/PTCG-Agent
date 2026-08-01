
def _update_internal_new_user_params(data_json: dict, data: NewUserRequest) -> dict:
    if "user_id" in data_json and data_json["user_id"] is None:
        data_json["user_id"] = str(uuid.uuid4())

    auto_create_key = data_json.pop("auto_create_key", True)

    if auto_create_key is False:
        data_json["table_name"] = (
            "user"  # only create a user, don't create key if 'auto_create_key' set to False
        )

    if litellm.default_internal_user_params and (
        data.user_role != LitellmUserRoles.PROXY_ADMIN.value
        and data.user_role != LitellmUserRoles.PROXY_ADMIN
    ):
        for key, value in litellm.default_internal_user_params.items():
            if key == "available_teams":
                continue
            elif key not in data_json or data_json[key] is None:
                data_json[key] = value
            elif (
                key == "models"
                and isinstance(data_json[key], list)
                and len(data_json[key]) == 0
            ):
                data_json[key] = value

    ## INTERNAL USER ROLE ONLY DEFAULT PARAMS ##
    if (
        data.user_role is not None
        and data.user_role == LitellmUserRoles.INTERNAL_USER.value
    ):
        if (
            litellm.max_internal_user_budget is not None
            and data_json.get("max_budget") is None
        ):
            data_json["max_budget"] = litellm.max_internal_user_budget

        if (
            litellm.internal_user_budget_duration is not None
            and data_json.get("budget_duration") is None
        ):
            data_json["budget_duration"] = litellm.internal_user_budget_duration

    data_json.pop("teams", None)  # handled separately
    return data_json

