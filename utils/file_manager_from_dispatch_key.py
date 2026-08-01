
def file_manager_from_dispatch_key(
    dispatch_key: DispatchKey,
    device_fms: dict[str, FileManager],
    default_fm: FileManager,
) -> FileManager:
    fm = device_fms.get(
        next(
            (
                device
                for check, device in dispatch_device_map.items()
                if check(dispatch_key)
            ),
            "",
        ),
        default_fm,
    )
    return fm

