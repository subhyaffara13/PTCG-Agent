
def _maybe_memory_map(
    handle: str | BaseBuffer, memory_map: bool
) -> tuple[str | BaseBuffer, bool, list[BaseBuffer]]:
    """Try to memory map file/buffer."""
    handles: list[BaseBuffer] = []
    memory_map &= hasattr(handle, "fileno") or isinstance(handle, str)
    if not memory_map:
        return handle, memory_map, handles

    # mmap used by only read_csv
    handle = cast(ReadCsvBuffer, handle)

    # need to open the file first
    if isinstance(handle, str):
        handle = open(handle, "rb")
        handles.append(handle)

    try:
        # open mmap and adds *-able
        # error: Argument 1 to "_IOWrapper" has incompatible type "mmap";
        # expected "BaseBuffer"
        wrapped = _IOWrapper(
            mmap.mmap(
                handle.fileno(),
                0,
                access=mmap.ACCESS_READ,  # type: ignore[arg-type]
            )
        )
    finally:
        for handle in reversed(handles):
            # error: "BaseBuffer" has no attribute "close"
            handle.close()  # type: ignore[attr-defined]

    return wrapped, memory_map, [wrapped]

