
def _get_dynamic_logging_metadata(
    user_api_key_dict: UserAPIKeyAuth, proxy_config: ProxyConfig
) -> Optional[TeamCallbackMetadata]:
    callback_settings_obj: Optional[TeamCallbackMetadata] = None
    key_dynamic_logging_settings: Optional[dict] = (
        KeyAndTeamLoggingSettings.get_key_dynamic_logging_settings(user_api_key_dict)
    )
    team_dynamic_logging_settings: Optional[dict] = (
        KeyAndTeamLoggingSettings.get_team_dynamic_logging_settings(user_api_key_dict)
    )
    #########################################################################################
    # Key-based callbacks
    #########################################################################################
    if key_dynamic_logging_settings is not None:
        for item in key_dynamic_logging_settings:
            callback = _get_validated_callback_metadata(item=item, source="key-level")
            if callback is None:
                continue
            callback_settings_obj = convert_key_logging_metadata_to_callback(
                data=callback,
                team_callback_settings_obj=callback_settings_obj,
            )
    #########################################################################################
    # Team-based callbacks
    #########################################################################################
    elif team_dynamic_logging_settings is not None:
        for item in team_dynamic_logging_settings:
            callback = _get_validated_callback_metadata(item=item, source="team-level")
            if callback is None:
                continue
            callback_settings_obj = convert_key_logging_metadata_to_callback(
                data=callback,
                team_callback_settings_obj=callback_settings_obj,
            )
    #########################################################################################
    # Deprecated format - maintained for backwards compatibility
    #########################################################################################
    elif (
        user_api_key_dict.team_metadata is not None
        and "callback_settings" in user_api_key_dict.team_metadata
    ):
        """
        callback_settings = {
            {
            'callback_vars': {'langfuse_public_key': 'pk', 'langfuse_secret_key': 'sk_'},
            'failure_callback': [],
            'success_callback': ['langfuse', 'langfuse']
        }
        }
        """
        team_metadata = decrypt_callback_vars(user_api_key_dict.team_metadata)
        callback_settings = team_metadata.get("callback_settings", None) or {}
        callback_settings_obj = TeamCallbackMetadata(**callback_settings)
        verbose_proxy_logger.debug(
            "Team callback settings activated: %s", callback_settings_obj
        )
    #########################################################################################
    # Enter here when configured on the config.yaml file.
    #########################################################################################
    elif user_api_key_dict.team_id is not None:
        callback_settings_obj = (
            LiteLLMProxyRequestSetup.add_team_based_callbacks_from_config(
                team_id=user_api_key_dict.team_id, proxy_config=proxy_config
            )
        )
    return callback_settings_obj

