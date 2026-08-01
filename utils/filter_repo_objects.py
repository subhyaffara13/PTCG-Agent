
def filter_repo_objects(
    items: Iterable[T],
    *,
    allow_patterns: list[str] | str | None = None,
    ignore_patterns: list[str] | str | None = None,
    key: Callable[[T], str] | None = None,
) -> Generator[T, None, None]:
    """Filter repo objects based on an allowlist and a denylist.

    Input must be a list of paths (`str` or `Path`) or a list of arbitrary objects.
    In the later case, `key` must be provided and specifies a function of one argument
    that is used to extract a path from each element in iterable.

    Patterns are Standard Wildcards (globbing patterns), NOT regular expressions.
    The pattern matching is based on Python's `fnmatch`. Note that `fnmatch` matches
    `*` across path boundaries, unlike traditional Unix shell globbing. For example,
    `"data/*.json"` will match both `data/file.json` and `data/subdir/file.json`.
    See https://docs.python.org/3/library/fnmatch.html for more details.

    Args:
        items (`Iterable`):
            List of items to filter.
        allow_patterns (`str` or `list[str]`, *optional*):
            Patterns constituting the allowlist. If provided, item paths must match at
            least one pattern from the allowlist.
        ignore_patterns (`str` or `list[str]`, *optional*):
            Patterns constituting the denylist. If provided, item paths must not match
            any patterns from the denylist.
        key (`Callable[[T], str]`, *optional*):
            Single-argument function to extract a path from each item. If not provided,
            the `items` must already be `str` or `Path`.

    Returns:
        Filtered list of objects, as a generator.

    Raises:
        :class:`ValueError`:
            If `key` is not provided and items are not `str` or `Path`.

    Example usage with paths:
    ```python
    >>> # Filter only PDFs that are not hidden.
    >>> list(filter_repo_objects(
    ...     ["aaa.PDF", "bbb.jpg", ".ccc.pdf", ".ddd.png"],
    ...     allow_patterns=["*.pdf"],
    ...     ignore_patterns=[".*"],
    ... ))
    ["aaa.pdf"]
    ```

    Example usage with objects:
    ```python
    >>> list(filter_repo_objects(
    ... [
    ...     CommitOperationAdd(path_or_fileobj="/tmp/aaa.pdf", path_in_repo="aaa.pdf")
    ...     CommitOperationAdd(path_or_fileobj="/tmp/bbb.jpg", path_in_repo="bbb.jpg")
    ...     CommitOperationAdd(path_or_fileobj="/tmp/.ccc.pdf", path_in_repo=".ccc.pdf")
    ...     CommitOperationAdd(path_or_fileobj="/tmp/.ddd.png", path_in_repo=".ddd.png")
    ... ],
    ... allow_patterns=["*.pdf"],
    ... ignore_patterns=[".*"],
    ... key=lambda x: x.repo_in_path
    ... ))
    [CommitOperationAdd(path_or_fileobj="/tmp/aaa.pdf", path_in_repo="aaa.pdf")]
    ```
    """
    if isinstance(allow_patterns, str):
        allow_patterns = [allow_patterns]

    if isinstance(ignore_patterns, str):
        ignore_patterns = [ignore_patterns]

    if allow_patterns is not None:
        allow_patterns = [_add_wildcard_to_directories(p) for p in allow_patterns]
    if ignore_patterns is not None:
        ignore_patterns = [_add_wildcard_to_directories(p) for p in ignore_patterns]

    if key is None:

        def _identity(item: T) -> str:
            if isinstance(item, str):
                return item
            if isinstance(item, Path):
                return str(item)
            raise ValueError(f"Please provide `key` argument in `filter_repo_objects`: `{item}` is not a string.")

        key = _identity  # Items must be `str` or `Path`, otherwise raise ValueError

    for item in items:
        path = key(item)

        # Skip if there's an allowlist and path doesn't match any
        if allow_patterns is not None and not any(fnmatch(path, r) for r in allow_patterns):
            continue

        # Skip if there's a denylist and path matches any
        if ignore_patterns is not None and any(fnmatch(path, r) for r in ignore_patterns):
            continue

        yield item

