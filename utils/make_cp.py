
def make_cp(context: CpContext | None = None):
    """Build the ``cp`` command function for a given alias.

    The three entry points (`hf cp`, `hf repos cp`, `hf buckets cp`) share the exact same logic;
    'context' only adds a guardrail on the remote endpoint type (see `_enforce_context`).
    """

    def cp(
        src: Annotated[
            str,
            typer.Argument(help="Source: local file, hf:// URI (repo or bucket), or - for stdin."),
        ],
        dst: Annotated[
            str | None,
            typer.Argument(help="Destination: local path, hf:// URI (repo or bucket), or - for stdout."),
        ] = None,
        token: TokenOpt = None,
    ) -> None:
        """Copy files between local paths, repositories, and buckets.

        Handles uploads (local/stdin -> repo/bucket), downloads (repo/bucket -> local/stdout) and
        remote-to-remote copies (repo/bucket -> repo/bucket). Bucket-to-repo and local-to-local
        copies are not supported. For directories, use `hf upload`/`hf download` (repos) or
        `hf buckets sync` (buckets). Remote-to-remote copies only work within the same storage
        region (https://huggingface.co/docs/hub/storage-regions).
        """
        _enforce_context(context, src, dst)
        _run_cp(src, dst, token)

    return cp

