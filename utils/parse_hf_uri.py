
def parse_hf_uri(uri: str, endpoint: str | None = None) -> HfUri:
    """Parse a Hugging Face Hub URI ('hf://...') or a Hugging Face web URL.

    A HF URI is a URI-like string identifying a location on the Hugging Face Hub. The full grammar is:

    ```
    hf://[<TYPE>/]<ID>[@<REVISION>][/<PATH>]
    ```

    For convenience, Hugging Face **web URLs** (the ones you copy-paste from the website) are also
    accepted and normalized to the canonical 'hf://' form, e.g.
    'https://huggingface.co/datasets/my-org/my-dataset/blob/main/train.csv'. Only unambiguous URLs
    (repository / bucket pages and file/folder viewer routes) are accepted; any other route is rejected.

    See 'docs/source/en/package_reference/hf_uris.md' for the full specification.

    Args:
        uri (`str`):
            The URI to parse. Must start with 'hf://', or be a Hugging Face URL (e.g. 'https://huggingface.co/...').
        endpoint (`str`, *optional*):
            A custom Hub endpoint (e.g. a self-hosted or proxied Hub like 'https://hub.my-company.com' or
            'http://localhost:8080/hf'). When provided, web URLs on that endpoint are recognized in addition to
            the default Hugging Face hosts. Has no effect on 'hf://' URIs.

    Returns:
        [`HfUri`]: the parsed URI.

    Raises:
        [`HfUriError`]:
            If the URI is malformed (missing prefix, invalid type, missing id, unsupported URL route, etc.).

    Examples:
        ```py
        >>> from huggingface_hub.utils import parse_hf_uri
        >>> parse_hf_uri("hf://my-org/my-model")
        HfUri(type='model', id='my-org/my-model', revision=None, path_in_repo='')
        >>> parse_hf_uri("hf://datasets/my-org/my-dataset@refs/pr/3/train.json")
        HfUri(type='dataset', id='my-org/my-dataset', revision='refs/pr/3', path_in_repo='train.json')
        >>> parse_hf_uri("https://huggingface.co/datasets/my-org/my-dataset/blob/main/train.csv")
        HfUri(type='dataset', id='my-org/my-dataset', revision='main', path_in_repo='train.csv')
        ```
    """
    raw = uri
    if uri.startswith(constants.HF_PROTOCOL):
        body = uri[len(constants.HF_PROTOCOL) :]
        if not body:
            raise HfUriError(uri, f"Empty body after '{constants.HF_PROTOCOL}'.")
    elif _looks_like_hf_url(uri, endpoint=endpoint):
        body = _url_to_uri_body(uri, endpoint=endpoint)
    else:
        raise HfUriError(
            uri,
            f"Must start with '{constants.HF_PROTOCOL}' or be a Hugging Face URL (e.g. 'https://huggingface.co/...'). "
            f"Expected format: {constants.HF_PROTOCOL}[<TYPE>/]<ID>[@<REVISION>][/<PATH>]",
        )

    type_, location = _split_type(body, raw=raw)

    if type_ == "bucket":
        return _parse_bucket_body(location, type_, raw=raw)
    return _parse_repo_body(location, type_, raw=raw)

