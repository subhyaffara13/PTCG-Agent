
def enable_triton(lib_dir: str | None = None) -> dict[str, str]:
    raise NotImplementedError(
        "`enable_triton` is deprecated. "
        "If you need NVSHMEM device function support for Triton, "
        "please use `@requires_nvshmem` to decorate your Triton kernel. ",
    )

