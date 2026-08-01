
def cleanup_router_config_variables():
    global master_key, user_config_file_path, otel_logging, user_custom_auth, user_custom_auth_path, user_custom_key_generate, user_custom_key_update, user_custom_sso, user_custom_ui_sso_sign_in_handler, use_background_health_checks, use_shared_health_check, health_check_interval, health_check_concurrency, prisma_client

    # Set all variables to None
    master_key = None
    user_config_file_path = None
    otel_logging = None
    user_custom_auth = None
    user_custom_auth_path = None
    user_custom_key_generate = None
    user_custom_key_update = None
    user_custom_sso = None
    user_custom_ui_sso_sign_in_handler = None
    use_background_health_checks = None
    use_shared_health_check = None
    health_check_interval = None
    health_check_concurrency = None
    prisma_client = None

