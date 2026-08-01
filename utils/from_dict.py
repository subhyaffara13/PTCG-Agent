
def from_dict(d):
    """Convert dict to dict-like NotebookNode

    Recursively converts any dict in the container to a NotebookNode.
    This does not check that the contents of the dictionary make a valid
    notebook or part of a notebook.
    """
    if isinstance(d, dict):
        return NotebookNode({k: from_dict(v) for k, v in d.items()})
    if isinstance(d, (tuple, list)):
        return [from_dict(i) for i in d]
    return d


def from_dict(d):
    """Create notebook node(s) from an object."""
    if isinstance(d, dict):
        newd = NotebookNode()
        for k, v in d.items():
            newd[k] = from_dict(v)
        return newd
    if isinstance(d, (tuple, list)):
        return [from_dict(i) for i in d]
    return d


def from_dict(d):
    """Create notebook node(s) from a value."""
    if isinstance(d, dict):
        newd = NotebookNode()
        for k, v in d.items():
            newd[k] = from_dict(v)
        return newd
    if isinstance(d, (tuple, list)):
        return [from_dict(i) for i in d]
    return d


def from_dict(d):
    """Create notebook node(s) from an object."""
    if isinstance(d, dict):
        newd = NotebookNode()
        for k, v in d.items():
            newd[k] = from_dict(v)
        return newd
    if isinstance(d, (tuple, list)):
        return [from_dict(i) for i in d]
    return d


def from_dict(data, require=None, use_rsa_signer=True):
    """Validates a dictionary containing Google service account data.

    Creates and returns a :class:`google.auth.crypt.Signer` instance from the
    private key specified in the data.

    Args:
        data (Mapping[str, str]): The service account data
        require (Sequence[str]): List of keys required to be present in the
            info.
        use_rsa_signer (Optional[bool]): Whether to use RSA signer or EC signer.
            We use RSA signer by default.

    Returns:
        google.auth.crypt.Signer: A signer created from the private key in the
            service account file.

    Raises:
        MalformedError: if the data was in the wrong format, or if one of the
            required keys is missing.
    """
    keys_needed = set(require if require is not None else [])

    missing = keys_needed.difference(data.keys())

    if missing:
        raise exceptions.MalformedError(
            "Service account info was not in the expected format, missing "
            "fields {}.".format(", ".join(missing))
        )

    # Create a signer.
    if use_rsa_signer:
        signer = crypt.RSASigner.from_service_account_info(data)
    else:
        signer = crypt.EsSigner.from_service_account_info(data)

    return signer

