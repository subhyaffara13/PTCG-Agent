
def parse_hf_mount(mount_str: str) -> HfMount:
    """Parse a HF mount specification ('hf://...:<MOUNT_PATH>[:ro|:rw]').

    A mount specification is a HF URI followed by a local mount path and an optional read-only/read-write flag.
    The full grammar is:

    ```
    hf://[<TYPE>/]<ID>[@<REVISION>][/<PATH>]:<MOUNT_PATH>[:ro|:rw]
    ```

    See 'docs/source/en/package_reference/hf_uris.md' for the full specification.

    Args:
        mount_str (`str`):
            The mount string to parse. Must start with 'hf://' and contain a ':<MOUNT_PATH>' segment.

    Returns:
        [`HfMount`]: the parsed mount.

    Raises:
        [`HfUriError`]:
            If the mount string is malformed (missing mount path, invalid URI, etc.).

    Examples:
        ```py
        >>> from huggingface_hub.utils import parse_hf_mount
        >>> parse_hf_mount("hf://my-org/my-model:/data:ro")
        HfMount(source=HfUri(type='model', id='my-org/my-model', revision=None, path_in_repo=''), mount_path='/data', read_only=True)
        >>> parse_hf_mount("hf://buckets/my-org/my-bucket/sub/dir:/mnt:rw")
        HfMount(source=HfUri(type='bucket', id='my-org/my-bucket', revision=None, path_in_repo='sub/dir'), mount_path='/mnt', read_only=False)
        ```
    """
    if not mount_str.startswith(constants.HF_PROTOCOL):
        raise HfUriError(
            uri=mount_str,
            msg=f"Must start with '{constants.HF_PROTOCOL}'.",
        )

    raw = mount_str
    body = mount_str[len(constants.HF_PROTOCOL) :]
    if not body:
        raise HfUriError(uri=raw, msg=f"Empty body after '{constants.HF_PROTOCOL}'.")

    location, mount_path, read_only = _split_mount(body, raw=raw)

    if mount_path is None:
        raise HfUriError(uri=raw, msg="Missing mount path. Expected ':<MOUNT_PATH>' (e.g. 'hf://org/model:/data').")

    # Re-assemble the URI part and parse it
    uri_str = constants.HF_PROTOCOL + location
    try:
        source = parse_hf_uri(uri_str)
    except HfUriError as e:
        raise HfUriError(uri=raw, msg=e.msg) from e

    return HfMount(source=source, mount_path=mount_path, read_only=read_only, _raw=raw)

