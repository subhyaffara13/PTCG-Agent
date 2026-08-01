
def create_metastore(options: Options, parallel_worker: bool) -> MetadataStore:
    """Create the appropriate metadata store."""
    if options.sqlite_cache:
        mds: MetadataStore = SqliteMetadataStore(
            _cache_dir_prefix(options),
            set_journal_mode=not parallel_worker,
            num_shards=options.sqlite_num_shards,
        )
    else:
        mds = FilesystemMetadataStore(_cache_dir_prefix(options))
    return mds

