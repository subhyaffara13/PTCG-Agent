
def _refresh_oauth_token_if_needed(token: str) -> str:
    """Refresh an OAuth access token if it is close to expiry. Best-effort: never raises.

    OAuth tokens obtained with the browser-based login are stored with a `refresh_token` and an
    `expires_at` timestamp (see `_save_token`). When the active token is one of them and about to
    expire, exchange the refresh token for a new access token and persist it. Any other token is
    returned unchanged.
    """
    global _OAUTH_REFRESH_CACHE
    with _OAUTH_REFRESH_LOCK:
        now = time.time()
        cache = _OAUTH_REFRESH_CACHE
        if cache is not None and cache["file_token"] == token and now < cache["recheck_at"]:
            return cache["resolved_token"]

        token_name, fields = next(
            ((name, fields) for name, fields in _read_stored_tokens_full().items() if fields.get("hf_token") == token),
            (None, {}),
        )
        refresh_token = fields.get("refresh_token")
        expires_at = _parse_expires_at(fields)
        if token_name is None or refresh_token is None or expires_at is None:
            # `token` may have just been replaced by a concurrent refresh (in which case it no
            # longer appears in the stored tokens): serve the fresh file token without caching.
            current_file_token = _get_token_from_file()
            if current_file_token is not None and current_file_token != token:
                return current_file_token
            # Not a refreshable OAuth token (or its metadata was lost): nothing to do.
            _OAUTH_REFRESH_CACHE = {
                "file_token": token,
                "resolved_token": token,
                "recheck_at": now + _OAUTH_RECHECK_INTERVAL,
            }
            return token

        if expires_at - _OAUTH_REFRESH_MARGIN > now:
            _OAUTH_REFRESH_CACHE = {
                "file_token": token,
                "resolved_token": token,
                "recheck_at": expires_at - _OAUTH_REFRESH_MARGIN,
            }
            return token

        try:
            # Cross-process file lock: if the server rotates refresh tokens, two processes
            # refreshing concurrently would invalidate each other's refresh token.
            with WeakFileLock(constants.HF_STORED_TOKENS_PATH + ".lock", timeout=30):
                # Re-read under the lock: another process may have refreshed in the meantime.
                fields = _read_stored_tokens_full().get(token_name, {})
                if fields.get("hf_token") != token:
                    # Another process already refreshed this token: adopt its result.
                    new_token = fields.get("hf_token") or token
                    new_expires_at = _parse_expires_at(fields)
                else:
                    response = refresh_access_token(refresh_token)
                    new_token = response["access_token"]
                    new_expires_at = int(now) + int(response["expires_in"]) if "expires_in" in response else None
                    _save_token(
                        token=new_token,
                        token_name=token_name,
                        # The server may rotate the refresh token; keep the old one if it doesn't.
                        refresh_token=response.get("refresh_token") or refresh_token,
                        expires_at=new_expires_at,
                    )
                    # Update the active token file, unless another process switched to a different token meanwhile.
                    if _get_token_from_file() == token:
                        _write_secret(Path(constants.HF_TOKEN_PATH), new_token)
                    logger.info(f"Access token `{token_name}` has been refreshed.")
        except Exception as e:
            if isinstance(e, DeviceCodeError) and e.error_code == OAuthErrorCode.INVALID_GRANT:
                # Refresh token expired or revoked: retrying is pointless, a re-login is required.
                # Warned unconditionally (the inf recheck guarantees it fires at most once): an
                # earlier transient warning must not suppress this actionable message.
                logger.warning(
                    "Your Hugging Face access token has expired and could not be refreshed "
                    f"(session expired or revoked). Run `hf auth login` to re-authenticate. ({e})"
                )
                recheck_at = float("inf")
            else:
                # Transient failure (offline, server error, ...): retry later.
                _warn_refresh_failure_once(f"Could not refresh your Hugging Face access token: {e}. Will retry later.")
                recheck_at = now + _OAUTH_RECHECK_INTERVAL
            # Return the existing token: if it's truly expired, the API will reject it with a clear error.
            _OAUTH_REFRESH_CACHE = {"file_token": token, "resolved_token": token, "recheck_at": recheck_at}
            return token

        _OAUTH_REFRESH_CACHE = {
            "file_token": new_token,
            "resolved_token": new_token,
            # The floor guards against a token lifetime shorter than the refresh margin, which
            # would otherwise put `recheck_at` in the past and trigger a refresh on every call.
            "recheck_at": max(
                now + _OAUTH_RECHECK_INTERVAL,
                new_expires_at - _OAUTH_REFRESH_MARGIN if new_expires_at else 0,
            ),
        }
        return new_token

