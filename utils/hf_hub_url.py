
def hf_hub_url(
    repo_id: str,
    filename: str,
    *,
    subfolder: str | None = None,
    repo_type: str | None = None,
    revision: str | None = None,
    endpoint: str | None = None,
) -> str:
    """Construct the URL of a file from the given information.

    The resolved address can either be a huggingface.co-hosted url, or a link to
    Cloudfront (a Content Delivery Network, or CDN) for large files which are
    more than a few MBs.

    Args:
        repo_id (`str`):
            A namespace (user or an organization) name and a repo name separated
            by a `/`.
        filename (`str`):
            The name of the file in the repo.
        subfolder (`str`, *optional*):
            An optional value corresponding to a folder inside the repo.
        repo_type (`str`, *optional*):
            Set to `"dataset"`, `"space"` or `"kernel"` if downloading from a dataset, space or kernel repo,
            `None` or `"model"` if downloading from a model. Default is `None`.
        revision (`str`, *optional*):
            An optional Git revision id which can be a branch name, a tag, or a
            commit hash.
        endpoint (`str`, *optional*):
            The Hub endpoint to send the request to. Defaults to the value of `HF_ENDPOINT`.

    Example:

    ```python
    >>> from huggingface_hub import hf_hub_url

    >>> hf_hub_url(
    ...     repo_id="julien-c/EsperBERTo-small", filename="pytorch_model.bin"
    ... )
    'https://huggingface.co/julien-c/EsperBERTo-small/resolve/main/pytorch_model.bin'
    ```

    > [!TIP]
    > Notes:
    >
    >     Cloudfront is replicated over the globe so downloads are way faster for
    >     the end user (and it also lowers our bandwidth costs).
    >
    >     Cloudfront aggressively caches files by default (default TTL is 24
    >     hours), however this is not an issue here because we implement a
    >     git-based versioning system on huggingface.co, which means that we store
    >     the files on S3/Cloudfront in a content-addressable way (i.e., the file
    >     name is its hash). Using content-addressable filenames means cache can't
    >     ever be stale.
    >
    >     In terms of client-side caching from this library, we base our caching
    >     on the objects' entity tag (`ETag`), which is an identifier of a
    >     specific version of a resource [1]_. An object's ETag is: its git-sha1
    >     if stored in git, or its sha256 if stored in git-lfs.

    References:

    -  [1] https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/ETag
    """
    if subfolder == "":
        subfolder = None
    if subfolder is not None:
        filename = f"{subfolder}/{filename}"

    if repo_type not in constants.REPO_TYPES_WITH_KERNEL:
        raise ValueError("Invalid repo type")

    if repo_type in constants.REPO_TYPES_URL_PREFIXES:
        repo_id = constants.REPO_TYPES_URL_PREFIXES[repo_type] + repo_id

    if revision is None:
        revision = constants.DEFAULT_REVISION
    url = constants.HUGGINGFACE_CO_URL_TEMPLATE.format(
        repo_id=repo_id, revision=quote(revision, safe=""), filename=quote(filename)
    )
    # Update endpoint if provided
    if endpoint is not None and url.startswith(constants.ENDPOINT):
        url = endpoint + url[len(constants.ENDPOINT) :]
    return url

