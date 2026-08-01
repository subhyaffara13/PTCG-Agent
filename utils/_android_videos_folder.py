
def _android_videos_folder() -> str:
    """:returns: videos folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415  # ty: ignore[unresolved-import]

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        videos_dir: str = context.getExternalFilesDir(environment.DIRECTORY_DCIM).getAbsolutePath()
    except Exception:  # noqa: BLE001
        videos_dir = "/storage/emulated/0/DCIM/Camera"

    return videos_dir


def _android_videos_folder() -> str:
    """:return: videos folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        videos_dir: str = context.getExternalFilesDir(environment.DIRECTORY_DCIM).getAbsolutePath()
    except Exception:  # noqa: BLE001
        videos_dir = "/storage/emulated/0/DCIM/Camera"

    return videos_dir


def _android_videos_folder() -> str:
    """:return: videos folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        videos_dir: str = context.getExternalFilesDir(environment.DIRECTORY_DCIM).getAbsolutePath()
    except Exception:  # noqa: BLE001
        videos_dir = "/storage/emulated/0/DCIM/Camera"

    return videos_dir

