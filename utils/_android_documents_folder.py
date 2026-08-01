
def _android_documents_folder() -> str:
    """:returns: documents folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415  # ty: ignore[unresolved-import]

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        documents_dir: str = context.getExternalFilesDir(environment.DIRECTORY_DOCUMENTS).getAbsolutePath()
    except Exception:  # noqa: BLE001
        documents_dir = "/storage/emulated/0/Documents"

    return documents_dir


def _android_documents_folder() -> str:
    """:return: documents folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        documents_dir: str = context.getExternalFilesDir(environment.DIRECTORY_DOCUMENTS).getAbsolutePath()
    except Exception:  # noqa: BLE001
        documents_dir = "/storage/emulated/0/Documents"

    return documents_dir


def _android_documents_folder() -> str:
    """:return: documents folder for the Android OS"""
    # Get directories with pyjnius
    try:
        from jnius import autoclass  # noqa: PLC0415

        context = autoclass("android.content.Context")
        environment = autoclass("android.os.Environment")
        documents_dir: str = context.getExternalFilesDir(environment.DIRECTORY_DOCUMENTS).getAbsolutePath()
    except Exception:  # noqa: BLE001
        documents_dir = "/storage/emulated/0/Documents"

    return documents_dir

