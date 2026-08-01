
def _add_mocked_oauth_routes(app: "fastapi.FastAPI", route_prefix: str = "/") -> None:
    """Add fake oauth routes if app is run locally and OAuth is enabled.

    Using OAuth will have the same behavior as in a Space but instead of authenticating with HF, a mocked user profile
    is added to the session.
    """
    try:
        import fastapi
        from fastapi.responses import RedirectResponse
        from starlette.datastructures import URL
    except ImportError as e:
        raise ImportError(
            "Cannot initialize OAuth to due a missing library. Please run `pip install huggingface_hub[oauth]` or add "
            "`huggingface_hub[oauth]` to your requirements.txt file."
        ) from e

    warnings.warn(
        "OAuth is not supported outside of a Space environment. To help you debug your app locally, the oauth endpoints"
        " are mocked to return your profile and token. To make it work, your machine must be logged in to Huggingface."
    )
    mocked_oauth_info = _get_mocked_oauth_info()

    login_uri, callback_uri, logout_uri = _get_oauth_uris(route_prefix)

    # Define OAuth routes
    @app.get(login_uri)
    async def oauth_login(request: fastapi.Request) -> RedirectResponse:
        """Fake endpoint that redirects to HF OAuth page."""
        # Define target (where to redirect after login)
        redirect_uri = _generate_redirect_uri(request)
        return RedirectResponse(callback_uri + "?" + urllib.parse.urlencode({"_target_url": redirect_uri}))

    @app.get(callback_uri)
    async def oauth_redirect_callback(request: fastapi.Request) -> RedirectResponse:
        """Endpoint that handles the OAuth callback."""
        request.session["oauth_info"] = mocked_oauth_info
        return RedirectResponse(_get_redirect_target(request))

    @app.get(logout_uri)
    async def oauth_logout(request: fastapi.Request) -> RedirectResponse:
        """Endpoint that logs out the user (e.g. delete cookie session)."""
        request.session.pop("oauth_info", None)
        logout_url = URL("/").include_query_params(**request.query_params)
        return RedirectResponse(url=logout_url, status_code=302)  # see https://github.com/gradio-app/gradio/pull/9659

