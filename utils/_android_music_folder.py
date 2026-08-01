
def _android_music_folder() -> str:
    """:returns: music folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415  # ty: ignore[unresolved-import]

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        music_dir: str = context.getExternalFilesDir(environment.DIRECTORY_MUSIC).getAbsolutePath()
    except Exception:  # noqa: BLE001
        music_dir = "/storage/emulated/0/Music"

    return music_dir


def _android_music_folder() -> str:
    """:return: music folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        music_dir: str = context.getExternalFilesDir(environment.DIRECTORY_MUSIC).getAbsolutePath()
    except Exception:  # noqa: BLE001
        music_dir = "/storage/emulated/0/Music"

    return music_dir


def _android_music_folder() -> str:
    """:return: music folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        music_dir: str = context.getExternalFilesDir(environment.DIRECTORY_MUSIC).getAbsolutePath()
    except Exception:  # noqa: BLE001
        music_dir = "/storage/emulated/0/Music"

    return music_dir

