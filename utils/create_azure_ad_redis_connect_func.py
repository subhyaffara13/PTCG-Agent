
def create_azure_ad_redis_connect_func(
    azure_client_id: Optional[str] = None,
    azure_tenant_id: Optional[str] = None,
    azure_client_secret: Optional[str] = None,
) -> Callable:
    """
    Creates a custom Redis connection function for Azure AD authentication.

    Used for sync Redis clients. The credential is created once (captured by the
    closure) and reused across connections — the Azure SDK handles token caching
    and silent renewal internally. Only ``get_token`` is called per connection.
    """
    credential = _build_azure_credential(
        azure_client_id=azure_client_id,
        azure_tenant_id=azure_tenant_id,
        azure_client_secret=azure_client_secret,
    )

    def ad_connect(self):
        """Initialize the connection and authenticate using Azure AD"""
        from redis.exceptions import (
            AuthenticationError,
            AuthenticationWrongNumberOfArgsError,
        )
        from redis.utils import str_if_bytes

        self._parser.on_connect(self)

        access_token = credential.get_token(AZURE_REDIS_SCOPE).token

        # Only include username when explicitly set — sending AUTH "" <token>
        # is invalid for most ACL-configured Azure Redis instances.
        username = os.environ.get("REDIS_USERNAME", "")
        if username:
            auth_args = (username, access_token)
        else:
            auth_args = (access_token,)

        self.send_command("AUTH", *auth_args, check_health=False)

        try:
            auth_response = self.read_response()
        except AuthenticationWrongNumberOfArgsError:
            # Fallback: try with just the token (Redis < 6 / no ACL)
            self.send_command("AUTH", access_token, check_health=False)
            auth_response = self.read_response()

        if str_if_bytes(auth_response) != "OK":
            raise AuthenticationError("Azure AD authentication failed for Redis")

    # Attach the live credential object so async paths can wrap it in
    # AzureADCredentialProvider for refresh-aware token retrieval. The raw
    # client_id/tenant_id/secret are intentionally NOT exposed here — the
    # credential closure already holds them.
    ad_connect._azure_credential = credential  # type: ignore[attr-defined]
    return ad_connect

