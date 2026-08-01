
def repo_type_and_id_from_hf_id(hf_id: str, hub_url: str | None = None) -> tuple[str | None, str | None, str]:
    """
    Returns the repo type and ID from a huggingface.co URL linking to a
    repository

    > [!WARNING]
    > Deprecated: prefer [`parse_hf_uri`], which parses both `hf://` URIs and Hugging Face web URLs into a structured [`HfUri`].
    > See https://huggingface.co/docs/huggingface_hub/package_reference/hf_uris for more details.

    Args:
        hf_id (`str`):
            An URL or ID of a repository on the HF hub. Accepted values are:

            - https://huggingface.co/<repo_type>/<namespace>/<repo_id>
            - https://huggingface.co/<namespace>/<repo_id>
            - hf://<repo_type>/<namespace>/<repo_id>
            - hf://<namespace>/<repo_id>
            - <repo_type>/<namespace>/<repo_id>
            - <namespace>/<repo_id>
            - <repo_id>
        hub_url (`str`, *optional*):
            The URL of the HuggingFace Hub, defaults to https://huggingface.co

    Returns:
        A tuple with three items: repo_type (`str` or `None`), namespace (`str` or
        `None`) and repo_id (`str`).

    Raises:
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If URL cannot be parsed.
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If `repo_type` is unknown.
    """
    input_hf_id = hf_id

    # Get the hub_url (with or without protocol)
    full_hub_url = hub_url if hub_url is not None else constants.ENDPOINT
    hub_url_without_protocol = _REGEX_HTTP_PROTOCOL.sub("", full_hub_url)

    # Check if hf_id is a URL containing the hub_url (check both with and without protocol)
    hf_id_without_protocol = _REGEX_HTTP_PROTOCOL.sub("", hf_id)
    is_hf_url = hub_url_without_protocol in hf_id_without_protocol and "@" not in hf_id

    HFFS_PREFIX = "hf://"
    if hf_id.startswith(HFFS_PREFIX):  # Remove "hf://" prefix if exists
        hf_id = hf_id[len(HFFS_PREFIX) :]

    # If it's a URL, strip the endpoint prefix to get the path
    if is_hf_url:
        # Remove protocol if present
        hf_id_normalized = _REGEX_HTTP_PROTOCOL.sub("", hf_id)

        # Remove the hub_url prefix to get the relative path
        if hf_id_normalized.startswith(hub_url_without_protocol):
            # Strip the hub URL and any leading slashes
            hf_id = hf_id_normalized[len(hub_url_without_protocol) :].lstrip("/")

    url_segments = hf_id.split("/")
    is_hf_id = len(url_segments) <= 3

    namespace: str | None
    if is_hf_url:
        # For URLs, we need to extract repo_type, namespace, repo_id
        # Expected format after stripping endpoint: [repo_type]/namespace/repo_id or namespace/repo_id

        if len(url_segments) >= 3:
            # Check if first segment is a repo type
            if url_segments[0] in constants.REPO_TYPES_MAPPING:
                repo_type = constants.REPO_TYPES_MAPPING[url_segments[0]]
                namespace = url_segments[1]
                repo_id = url_segments[2]
            elif url_segments[0] == "buckets":
                # Special case for buckets
                repo_type = "bucket"
                namespace = url_segments[1]
                repo_id = url_segments[2]
            else:
                # First segment is namespace
                namespace = url_segments[0]
                repo_id = url_segments[1]
                repo_type = None
        elif len(url_segments) == 2:
            namespace = url_segments[0]
            repo_id = url_segments[1]

            # Check if namespace is actually a repo type mapping
            if namespace in constants.REPO_TYPES_MAPPING:
                # Mean canonical dataset or model
                repo_type = constants.REPO_TYPES_MAPPING[namespace]
                namespace = None
            elif namespace == "buckets":
                # Special case for buckets
                repo_type = "bucket"
                namespace = None
            else:
                repo_type = None
        else:
            # Single segment
            repo_id = url_segments[0]
            namespace = None
            repo_type = None
    elif is_hf_id:
        if len(url_segments) == 3:
            # Passed <repo_type>/<user>/<model_id> or <repo_type>/<org>/<model_id>
            repo_type, namespace, repo_id = url_segments[-3:]
        elif len(url_segments) == 2:
            if url_segments[0] in constants.REPO_TYPES_MAPPING:
                # Passed '<model_id>' or 'datasets/<dataset_id>' for a canonical model or dataset
                repo_type = constants.REPO_TYPES_MAPPING[url_segments[0]]
                namespace = None
                repo_id = hf_id.split("/")[-1]
            elif url_segments[0] == "buckets":
                # Special case for buckets
                repo_type = "bucket"
                namespace = None
                repo_id = hf_id.split("/")[-1]
            else:
                # Passed <user>/<model_id> or <org>/<model_id>
                namespace, repo_id = hf_id.split("/")[-2:]
                repo_type = None
        else:
            # Passed <model_id>
            repo_id = url_segments[0]
            namespace, repo_type = None, None
    else:
        raise ValueError(f"Unable to retrieve user and repo ID from the passed HF ID: {hf_id}")

    # Check if repo type is known (mapping "spaces" => "space" + empty value => `None`)
    if repo_type in constants.REPO_TYPES_MAPPING:
        repo_type = constants.REPO_TYPES_MAPPING[repo_type]
    if repo_type == "":
        repo_type = None
    if repo_type not in constants.REPO_TYPES_WITH_KERNEL and repo_type != "bucket":
        raise ValueError(f"Unknown `repo_type`: '{repo_type}' ('{input_hf_id}')")

    return repo_type, namespace, repo_id

