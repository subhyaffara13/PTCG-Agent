
def common_key_access_checks(
    user_api_key_dict: UserAPIKeyAuth,
    data: Union[GenerateKeyRequest, UpdateKeyRequest],
    llm_router: Optional[Router],
    premium_user: bool,
    user_id: Optional[str] = None,
) -> Literal[True]:
    """
    Check if user is allowed to make a key request, for this key
    """
    try:
        _is_allowed_to_make_key_request(
            user_api_key_dict=user_api_key_dict,
            user_id=user_id or data.user_id,
            team_id=data.team_id,
        )
    except AssertionError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    _check_model_access_group(
        models=data.models,
        llm_router=llm_router,
        premium_user=premium_user,
    )
    return True

