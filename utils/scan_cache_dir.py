from pathlib import Path


def scan_cache_dir(cache_dir: str | Path | None = None) -> HFCacheInfo:
    """Scan the entire HF cache-system and return a [`~HFCacheInfo`] structure.

    Use `scan_cache_dir` in order to programmatically scan your cache-system. The cache
    will be scanned repo by repo. If a repo is corrupted, a [`~CorruptedCacheException`]
    will be thrown internally but captured and returned in the [`~HFCacheInfo`]
    structure. Only valid repos get a proper report.

    ```py
    >>> from huggingface_hub import scan_cache_dir

    >>> hf_cache_info = scan_cache_dir()
    HFCacheInfo(
        size_on_disk=3398085269,
        repos=frozenset({
            CachedRepoInfo(
                repo_id='t5-small',
                repo_type='model',
                repo_path=PosixPath(...),
                size_on_disk=970726914,
                nb_files=11,
                revisions=frozenset({
                    CachedRevisionInfo(
                        commit_hash='d78aea13fa7ecd06c29e3e46195d6341255065d5',
                        size_on_disk=970726339,
                        snapshot_path=PosixPath(...),
                        files=frozenset({
                            CachedFileInfo(
                                file_name='config.json',
                                size_on_disk=1197
                                file_path=PosixPath(...),
                                blob_path=PosixPath(...),
                            ),
                            CachedFileInfo(...),
                            ...
                        }),
                    ),
                    CachedRevisionInfo(...),
                    ...
                }),
            ),
            CachedRepoInfo(...),
            ...
        }),
        warnings=[
            CorruptedCacheException("Snapshots dir doesn't exist in cached repo: ..."),
            CorruptedCacheException(...),
            ...
        ],
    )
    ```

    You can also print a detailed report directly from the `hf` command line using:
    ```text
    > hf cache ls
    ID                          SIZE     LAST_ACCESSED LAST_MODIFIED REFS
    --------------------------- -------- ------------- ------------- -----------
    dataset/nyu-mll/glue          157.4M 2 days ago    2 days ago    main script
    model/LiquidAI/LFM2-VL-1.6B     3.2G 4 days ago    4 days ago    main
    model/microsoft/UserLM-8b      32.1G 4 days ago    4 days ago    main

    Done in 0.0s. Scanned 6 repo(s) for a total of 3.4G.
    Got 1 warning(s) while scanning. Use -vvv to print details.
    ```

    Args:
        cache_dir (`str` or `Path`, `optional`):
            Cache directory to cache. Defaults to the default HF cache directory.

    > [!WARNING]
    > Raises:
    >
    >     `CacheNotFound`
    >       If the cache directory does not exist.
    >
    >     [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
    >       If the cache directory is a file, instead of a directory.

    Returns: a [`~HFCacheInfo`] object.
    """
    if cache_dir is None:
        cache_dir = HF_HUB_CACHE

    cache_dir = Path(cache_dir).expanduser().resolve()
    if not cache_dir.exists():
        raise CacheNotFound(
            f"Cache directory not found: {cache_dir}. Please use `cache_dir` argument or set `HF_HUB_CACHE` environment variable.",
            cache_dir=cache_dir,
        )

    if cache_dir.is_file():
        raise ValueError(
            f"Scan cache expects a directory but found a file: {cache_dir}. Please use `cache_dir` argument or set `HF_HUB_CACHE` environment variable."
        )

    repos: set[CachedRepoInfo] = set()
    warnings: list[CorruptedCacheException] = []
    for repo_path in cache_dir.iterdir():
        if repo_path.name in FILES_TO_IGNORE:
            continue
        if repo_path.name == ".locks":  # skip './.locks/' folder
            continue
        if repo_path.name == "CACHEDIR.TAG":  # skip CACHEDIR.TAG file
            continue
        try:
            repos.add(_scan_cached_repo(repo_path))
        except CorruptedCacheException as e:
            warnings.append(e)

    return HFCacheInfo(
        repos=frozenset(repos),
        size_on_disk=sum(repo.size_on_disk for repo in repos),
        warnings=warnings,
    )

