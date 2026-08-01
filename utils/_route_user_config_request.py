
def _route_user_config_request(data: dict, route_type: str):
    """Route a request using the user-provided router config."""
    router_config = data.pop("user_config")

    # Filter router_config to only include valid Router.__init__ arguments
    # This prevents TypeError when invalid parameters are stored in the database
    valid_args = litellm.Router.get_valid_args()
    filtered_config = {k: v for k, v in router_config.items() if k in valid_args}

    user_router = litellm.Router(**filtered_config)
    ret_val = getattr(user_router, f"{route_type}")(**data)
    user_router.discard()
    return ret_val

