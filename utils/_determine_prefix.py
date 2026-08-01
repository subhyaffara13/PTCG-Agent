
def _determine_prefix(files: list[str]) -> str:
    """If the user doesn't specify a prefix, but does pass a dir full of similarly-prefixed files, we should be able to
    infer the common prefix most of the time.  But if we can't confidently infer, just fall back to requiring the user
    to specify it
    """
    possible_prefixes: defaultdict[str, set[int]] = defaultdict(set)
    for f in files:
        m = exp.search(f)
        if m:
            p, r = m.groups()
            possible_prefixes[p].add(int(r))
    if len(possible_prefixes) == 1:
        prefix = next(iter(possible_prefixes))
        logger.debug("Inferred common prefix %s", prefix)
        return prefix
    else:
        raise ValueError(
            "Unable to automatically determine the common prefix for the trace file names. "
            "Please specify --prefix argument manually"
        )

