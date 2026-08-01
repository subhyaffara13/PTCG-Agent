
def _proxy_server_imports():
    from litellm.proxy.proxy_server import (  # noqa: PLC0415
        general_settings,
        llm_router,
        proxy_config,
        proxy_logging_obj,
        select_data_generator,
        user_api_base,
        user_max_tokens,
        user_model,
        user_request_timeout,
        user_temperature,
        version,
    )

    return dict(
        general_settings=general_settings,
        llm_router=llm_router,
        proxy_config=proxy_config,
        proxy_logging_obj=proxy_logging_obj,
        select_data_generator=select_data_generator,
        user_api_base=user_api_base,
        user_max_tokens=user_max_tokens,
        user_model=user_model,
        user_request_timeout=user_request_timeout,
        user_temperature=user_temperature,
        version=version,
    )

