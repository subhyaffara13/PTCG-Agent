
def _download_image_sync(url: str) -> Tuple[bytes, str, str]:
    """Download image from URL synchronously."""
    client = _get_httpx_client(params={"ssl_verify": False})
    response = client.get(url)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "image/jpeg")
    ext = content_type.split("/")[-1].split(";")[0] or "jpg"

    return response.content, content_type, ext

