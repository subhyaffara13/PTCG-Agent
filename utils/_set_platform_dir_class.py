import os

def _set_platform_dir_class() -> type[PlatformDirsABC]:
    if os.getenv("ANDROID_DATA") == "/data" and os.getenv("ANDROID_ROOT") == "/system":
        if os.getenv("SHELL") or os.getenv("PREFIX"):
            return _Result

        from platformdirs.android import _android_folder  # noqa: PLC0415

        if _android_folder() is not None:
            from platformdirs.android import Android  # noqa: PLC0415

            return Android  # return to avoid redefinition of a result

    return _Result


def _set_platform_dir_class() -> type[PlatformDirsABC]:
    if os.getenv("ANDROID_DATA") == "/data" and os.getenv("ANDROID_ROOT") == "/system":
        if os.getenv("SHELL") or os.getenv("PREFIX"):
            return _Result

        from platformdirs.android import _android_folder  # noqa: PLC0415

        if _android_folder() is not None:
            from platformdirs.android import Android  # noqa: PLC0415

            return Android  # return to avoid redefinition of a result

    return _Result


def _set_platform_dir_class() -> type[PlatformDirsABC]:
    if os.getenv("ANDROID_DATA") == "/data" and os.getenv("ANDROID_ROOT") == "/system":
        if os.getenv("SHELL") or os.getenv("PREFIX"):
            return _Result

        from pip._vendor.platformdirs.android import _android_folder  # noqa: PLC0415

        if _android_folder() is not None:
            from pip._vendor.platformdirs.android import Android  # noqa: PLC0415

            return Android  # return to avoid redefinition of a result

    return _Result

