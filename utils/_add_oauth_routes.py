
def _add_oauth_routes(app: "fastapi.FastAPI", route_prefix: str) -> None:
    """Add OAuth routes to the FastAPI app (login, callback handler and logout)."""
    try:
        import fastapi
        from authlib.integrations.base_client.errors import MismatchingStateError
        from authlib.integrations.starlette_client import OAuth
        from fastapi.responses import RedirectResponse
    except ImportError as e:
        raise ImportError(
            "Cannot initialize OAuth to due a missing library. Please run `pip install huggingface_hub[oauth]` or add "
            "`huggingface_hub[oauth]` to your requirements.txt file."
        ) from e

    # Check environment variables
    msg = (
        "OAuth is required but '{}' environment variable is not set. Make sure you've enabled OAuth in your Space by"
        " setting `hf_oauth: true` in the Space metadata."
    )
    if constants.OAUTH_CLIENT_ID is None:
        raise ValueError(msg.format("OAUTH_CLIENT_ID"))
    if constants.OAUTH_CLIENT_SECRET is None:
        raise ValueError(msg.format("OAUTH_CLIENT_SECRET"))
    if constants.OAUTH_SCOPES is None:
        raise ValueError(msg.format("OAUTH_SCOPES"))
    if constants.OPENID_PROVIDER_URL is None:
        raise ValueError(msg.format("OPENID_PROVIDER_URL"))

    # Register OAuth server
    oauth = OAuth()
    oauth.register(
        name="huggingface",
        client_id=constants.OAUTH_CLIENT_ID,
        client_secret=constants.OAUTH_CLIENT_SECRET,
        client_kwargs={"scope": constants.OAUTH_SCOPES},
        server_metadata_url=constants.OPENID_PROVIDER_URL + "/.well-known/openid-configuration",
    )

    login_uri, callback_uri, logout_uri = _get_oauth_uris(route_prefix)

    # Register OAuth endpoints
    @app.get(login_uri)
    async def oauth_login(request: fastapi.Request) -> RedirectResponse:
        """Endpoint that redirects to HF OAuth page."""
        redirect_uri = _generate_redirect_uri(request)
        return await oauth.huggingface.authorize_redirect(request, redirect_uri)  # type: ignore

    @app.get(callback_uri)
    async def oauth_redirect_callback(request: fastapi.Request) -> RedirectResponse:
        """Endpoint that handles the OAuth callback."""
        try:
            oauth_info = await oauth.huggingface.authorize_access_token(request)  # type: ignore
        except MismatchingStateError:
            # Parse query params
            nb_redirects = int(request.query_params.get("_nb_redirects", 0))
            target_url = request.query_params.get("_target_url")

            # Build redirect URI with the same query params as before and bump nb_redirects count
            query_params: dict[str, int | str] = {"_nb_redirects": nb_redirects + 1}
            if target_url:
                query_params["_target_url"] = target_url

            redirect_uri = f"{login_uri}?{urllib.parse.urlencode(query_params)}"

            # If the user is redirected more than 3 times, it is very likely that the cookie is not working properly.
            # (e.g. browser is blocking third-party cookies in iframe). In this case, redirect the user in the
            # non-iframe view.
            if nb_redirects > constants.OAUTH_MAX_REDIRECTS:
                host = os.environ.get("SPACE_HOST")
                if host is None:  # cannot happen in a Space
                    raise RuntimeError(
                        "App is not running in a Space (SPACE_HOST environment variable is not set). Cannot redirect to non-iframe view."
                    ) from None
                host_url = "https://" + host.rstrip("/")
                return RedirectResponse(host_url + redirect_uri)

            # Redirect the user to the login page again
            return RedirectResponse(redirect_uri)

        # OAuth login worked => store the user info in the session and redirect
        logger.debug("Successfully logged in with OAuth. Storing user info in session.")
        request.session["oauth_info"] = oauth_info
        return RedirectResponse(_get_redirect_target(request))

    @app.get(logout_uri)
    async def oauth_logout(request: fastapi.Request) -> RedirectResponse:
        """Endpoint that logs out the user (e.g. delete info from cookie session)."""
        logger.debug("Logged out with OAuth. Removing user info from session.")
        request.session.pop("oauth_info", None)
        return RedirectResponse(_get_redirect_target(request))

