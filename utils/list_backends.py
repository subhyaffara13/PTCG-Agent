
def list_backends(exclude_tags=("debug", "experimental")) -> list[str]:
    """
    Return valid strings that can be passed to `torch.compile(..., backend="name")`.

    Args:
        exclude_tags(optional): A tuple of strings representing tags to exclude.
    """
    import torch._dynamo

    return torch._dynamo.list_backends(exclude_tags)


def list_backends(exclude_tags=("debug", "experimental")) -> list[str]:  # type: ignore[no-untyped-def]
    """
    Return valid strings that can be passed to:

        torch.compile(..., backend="name")
    """
    _lazy_import()
    exclude_tags_set = set(exclude_tags or ())

    backends = [
        name
        for name in _BACKENDS
        if name not in _COMPILER_FNS
        or not exclude_tags_set.intersection(_COMPILER_FNS[name]._tags)  # type: ignore[attr-defined]
    ]
    return sorted(backends)

