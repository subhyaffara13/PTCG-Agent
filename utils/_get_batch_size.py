
def _get_batch_size(nofiles=False):
    from fsspec.config import conf

    if nofiles:
        if "nofiles_gather_batch_size" in conf:
            return conf["nofiles_gather_batch_size"]
    else:
        if "gather_batch_size" in conf:
            return conf["gather_batch_size"]
    if nofiles:
        return _NOFILES_DEFAULT_BATCH_SIZE
    if resource is None:
        return _DEFAULT_BATCH_SIZE

    try:
        soft_limit, _ = resource.getrlimit(resource.RLIMIT_NOFILE)
    except (ImportError, ValueError, ResourceError):
        return _DEFAULT_BATCH_SIZE

    if soft_limit == resource.RLIM_INFINITY:
        return -1
    else:
        return soft_limit // 8

