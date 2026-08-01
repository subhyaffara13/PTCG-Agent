
def select_data_generator(
    response,
    user_api_key_dict: UserAPIKeyAuth,
    request_data: dict,
    request: Request | None = None,
):
    return async_data_generator(
        response=response,
        user_api_key_dict=user_api_key_dict,
        request_data=request_data,
        request=request,
    )

