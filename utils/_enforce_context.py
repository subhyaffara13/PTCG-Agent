
def _enforce_context(context: CpContext | None, src: str, dst: str | None) -> None:
    """Guardrail for the `hf repos cp` / `hf buckets cp` aliases.

    These aliases are exact duplicates of `hf cp`, so a bare `hf repos cp` could otherwise touch a
    bucket (and vice versa). We validate the type of the remote side: the destination for uploads and
    remote-to-remote copies, or the source when downloading to a local path / stdout. The top-level
    `hf cp` (i.e. 'context' is None) accepts any combination.
    """
    if context is None:
        return
    # The remote endpoint is the destination when it is an hf:// URI, otherwise the source (download).
    remote = dst if (dst is not None and is_hf_uri(dst)) else src
    if not is_hf_uri(remote):
        return
    if context == "repos" and parse_hf_uri(remote).is_bucket:
        raise CLIError("`hf repos cp` only works with repositories. Use `hf cp` or `hf buckets cp` for buckets.")
    if context == "buckets" and not parse_hf_uri(remote).is_bucket:
        raise CLIError("`hf buckets cp` only works with buckets. Use `hf cp` or `hf repos cp` for repositories.")

