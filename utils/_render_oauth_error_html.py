from typing import Optional

def _render_oauth_error_html(error: str, description: Optional[str]) -> HTMLResponse:
    """Render an actionable HTML page for an IdP-reported OAuth error.

    Used when we cannot propagate the error back to the registered
    ``redirect_uri`` (state missing or undecryptable). Returned with a 400
    status so the failure is observable to operators while still being a
    human-readable page for the end user.
    """
    safe_error = _html.escape(error or "unknown_error")
    safe_description = _html.escape(description) if description else ""
    description_html = f"<p>{safe_description}</p>" if safe_description else ""
    body = (
        "<html><body>"
        "<h2>Authentication failed</h2>"
        f"<p><strong>Error:</strong> {safe_error}</p>"
        f"{description_html}"
        "<p>You can close this window and try again.</p>"
        "</body></html>"
    )
    return HTMLResponse(body, status_code=400)

