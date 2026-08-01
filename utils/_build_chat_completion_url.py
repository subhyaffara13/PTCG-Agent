
def _build_chat_completion_url(model_url: str) -> str:
    # Strip trailing /
    model_url = model_url.rstrip("/")

    # Append /chat/completions if not already present
    if model_url.endswith("/v1"):
        model_url += "/chat/completions"

    # Append /v1/chat/completions if not already present
    if not model_url.endswith("/chat/completions"):
        model_url += "/v1/chat/completions"

    return model_url


def _build_chat_completion_url(model_url: str) -> str:
    parsed = urlparse(model_url)
    path = parsed.path.rstrip("/")

    # If the path already ends with /chat/completions, we're done!
    if path.endswith("/chat/completions"):
        return model_url

    # Append /chat/completions if not already present
    if path.endswith("/v1"):
        new_path = path + "/chat/completions"
    # If path was empty or just "/", set the full path
    elif not path:
        new_path = "/v1/chat/completions"
    # Append /v1/chat/completions if not already present
    else:
        new_path = path + "/v1/chat/completions"

    # Reconstruct the URL with the new path and original query parameters.
    new_parsed = parsed._replace(path=new_path)
    return str(urlunparse(new_parsed))

