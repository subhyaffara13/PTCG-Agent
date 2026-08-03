import os

def get_logo_url():
    """Get the current logo URL from environment.

    Only HTTP(S) URLs are returned — those are intended to be loaded
    directly by the browser from a public/internal CDN. Local file
    paths set via ``UI_LOGO_PATH`` are NOT returned: they are admin-
    only filesystem details, the dashboard falls back to ``/get_image``
    which serves the file only when it is a supported image. Without
    this filter, the unauthenticated endpoint would disclose internal
    hostnames or filesystem paths to any caller.
    """
    logo_path = os.getenv("UI_LOGO_PATH", "")
    if logo_path.startswith(("http://", "https://")):
        return {"logo_url": logo_path}
    return {"logo_url": ""}

