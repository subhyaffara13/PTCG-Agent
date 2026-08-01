
def _android_pictures_folder() -> str:
    """:returns: pictures folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415  # ty: ignore[unresolved-import]

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        pictures_dir: str = context.getExternalFilesDir(environment.DIRECTORY_PICTURES).getAbsolutePath()
    except Exception:  # noqa: BLE001
        pictures_dir = "/storage/emulated/0/Pictures"

    return pictures_dir


def _android_pictures_folder() -> str:
    """:return: pictures folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        pictures_dir: str = context.getExternalFilesDir(environment.DIRECTORY_PICTURES).getAbsolutePath()
    except Exception:  # noqa: BLE001
        pictures_dir = "/storage/emulated/0/Pictures"

    return pictures_dir


def _android_pictures_folder() -> str:
    """:return: pictures folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        pictures_dir: str = context.getExternalFilesDir(environment.DIRECTORY_PICTURES).getAbsolutePath()
    except Exception:  # noqa: BLE001
        pictures_dir = "/storage/emulated/0/Pictures"

    return pictures_dir

