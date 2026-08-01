
def _resolve_proxy_base_for_redirect(request: Request) -> Optional[str]:
    try:
        return get_request_base_url(request)
    except Exception as exc:
        verbose_logger.warning(
            "validate_trusted_redirect_uri: could not determine proxy origin, "
            "falling back to loopback + allowlist. error=%s",
            exc,
        )
        return None

