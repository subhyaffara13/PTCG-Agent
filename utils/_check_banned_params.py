
def _check_banned_params(
    body: dict,
    general_settings: dict,
    llm_router: Optional[Router],
    model: str,
) -> None:
    """Raise ``ValueError`` if ``body`` carries a banned param without admin opt-in.

    Shared between the root-level check and the nested-config check so a
    new banned param only needs to be added in one place.
    """
    for param in _BANNED_REQUEST_BODY_PARAMS:
        if param not in body:
            continue
        if general_settings.get("allow_client_side_credentials") is True:
            # Proxy-wide opt-in: every banned param is permitted, exit
            # entirely so the rest of the loop doesn't waste work.
            return
        if (
            _allow_model_level_clientside_configurable_parameters(
                model=model,
                param=param,
                request_body_value=body[param],
                llm_router=llm_router,
            )
            is True
        ):
            # Per-param opt-in: only THIS param is permitted by the
            # deployment's ``configurable_clientside_auth_params``. Skip
            # to the next banned param so a body that pairs an allowed
            # ``api_base`` with an unallowed ``langfuse_host`` is still
            # rejected for the second field.
            continue
        raise ValueError(
            f"Rejected Request: {param} is not allowed in request body. "
            "Clientside passthrough requires explicit admin opt-in via "
            "either `general_settings.allow_client_side_credentials = true` "
            "(proxy-wide) or `configurable_clientside_auth_params` on the "
            "deployment in your proxy config.yaml. "
            "Relevant Issue: https://huntr.com/bounties/4001e1a2-7b7a-4776-a3ae-e6692ec3d997",
        )

