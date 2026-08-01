
def attach_huggingface_oauth(app: "fastapi.FastAPI", route_prefix: str = "/"):
    """
    Add OAuth endpoints to a FastAPI app to enable OAuth login with Hugging Face.

    How to use:
    - Call this method on your FastAPI app to add the OAuth endpoints.
    - Inside your route handlers, call `parse_huggingface_oauth(request)` to retrieve the OAuth info.
    - If user is logged in, an [`OAuthInfo`] object is returned with the user's info. If not, `None` is returned.
    - In your app, make sure to add links to `/oauth/huggingface/login` and `/oauth/huggingface/logout` for the user to log in and out.

    Example:
    ```py
    from huggingface_hub import attach_huggingface_oauth, parse_huggingface_oauth

    # Create a FastAPI app
    app = FastAPI()

    # Add OAuth endpoints to the FastAPI app
    attach_huggingface_oauth(app)

    # Add a route that greets the user if they are logged in
    @app.get("/")
    def greet_json(request: Request):
        # Retrieve the OAuth info from the request
        oauth_info = parse_huggingface_oauth(request)  # e.g. OAuthInfo dataclass
        if oauth_info is None:
            return {"msg": "Not logged in!"}
        return {"msg": f"Hello, {oauth_info.user_info.preferred_username}!"}
    ```
    """
    # TODO: handle generic case (handling OAuth in a non-Space environment with custom dev values) (low priority)

    # Add SessionMiddleware to the FastAPI app to store the OAuth info in the session.
    # Session Middleware requires a secret key to sign the cookies. Let's use a hash
    # of the OAuth secret key to make it unique to the Space + updated in case OAuth
    # config gets updated. When ran locally, we use an empty string as a secret key.
    try:
        from starlette.middleware.sessions import SessionMiddleware
    except ImportError as e:
        raise ImportError(
            "Cannot initialize OAuth to due a missing library. Please run `pip install huggingface_hub[oauth]` or add "
            "`huggingface_hub[oauth]` to your requirements.txt file in order to install the required dependencies."
        ) from e
    session_secret = (constants.OAUTH_CLIENT_SECRET or "") + "-v1"
    app.add_middleware(
        SessionMiddleware,  # type: ignore
        secret_key=hashlib.sha256(session_secret.encode()).hexdigest(),
        same_site="none",
        https_only=True,
    )  # type: ignore

    # Add OAuth endpoints to the FastAPI app:
    #   - {route_prefix}/oauth/huggingface/login
    #   - {route_prefix}/oauth/huggingface/callback
    #   - {route_prefix}/oauth/huggingface/logout
    # If the app is running in a Space, OAuth is enabled normally.
    # Otherwise, we mock the endpoints to make the user log in with a fake user profile - without any calls to hf.co.
    route_prefix = route_prefix.strip("/")
    if os.getenv("SPACE_ID") is not None:
        logger.info("OAuth is enabled in the Space. Adding OAuth routes.")
        _add_oauth_routes(app, route_prefix=route_prefix)
    else:
        logger.info("App is not running in a Space. Adding mocked OAuth routes.")
        _add_mocked_oauth_routes(app, route_prefix=route_prefix)

