import re
import sys

def _android_folder() -> str | None:  # noqa: C901
    """:returns: base folder for the Android OS or None if it cannot be found"""
    result: str | None = None
    # type checker isn't happy with our "import android", just don't do this when type checking see
    # https://stackoverflow.com/a/61394121
    if not TYPE_CHECKING:
        try:
            # First try to get a path to android app using python4android (if available)...
            from android import mActivity  # noqa: PLC0415

            context = cast("android.content.Context", mActivity.getApplicationContext())  # noqa: F821
            result = context.getFilesDir().getParentFile().getAbsolutePath()
        except Exception:  # noqa: BLE001
            result = None
    if result is None:
        try:
            # ...and fall back to using plain pyjnius, if python4android isn't available or doesn't deliver any useful
            # result...
            from jnius import autoclass  # noqa: PLC0415  # ty: ignore[unresolved-import]

            context = autoclass("android.content.Context")
            result = context.getFilesDir().getParentFile().getAbsolutePath()
        except Exception:  # noqa: BLE001
            result = None
    if result is None:
        # and if that fails, too, find an android folder looking at path on the sys.path
        # warning: only works for apps installed under /data, not adopted storage etc.
        pattern = re.compile(r"/data/(data|user/\d+)/(.+)/files")
        for path in sys.path:
            if pattern.match(path):
                result = path.split("/files")[0]
                break
        else:
            result = None
    if result is None:
        # one last try: find an android folder looking at path on the sys.path taking adopted storage paths into
        # account
        pattern = re.compile(r"/mnt/expand/[a-fA-F0-9-]{36}/(data|user/\d+)/(.+)/files")
        for path in sys.path:
            if pattern.match(path):
                result = path.split("/files")[0]
                break
        else:
            result = None
    return result


def _android_folder() -> str | None:  # noqa: C901
    """:return: base folder for the Android OS or None if it cannot be found"""
    result: str | None = None
    # type checker isn't happy with our "import android", just don't do this when type checking see
    # https://stackoverflow.com/a/61394121
    if not TYPE_CHECKING:
        try:
            # First try to get a path to android app using python4android (if available)...
            from android import mActivity  # noqa: PLC0415

            context = cast("android.content.Context", mActivity.getApplicationContext())  # noqa: F821
            result = context.getFilesDir().getParentFile().getAbsolutePath()
        except Exception:  # noqa: BLE001
            result = None
    if result is None:
        try:
            # ...and fall back to using plain pyjnius, if python4android isn't available or doesn't deliver any useful
            # result...
            from jnius import autoclass  # noqa: PLC0415

            context = autoclass("android.content.Context")
            result = context.getFilesDir().getParentFile().getAbsolutePath()
        except Exception:  # noqa: BLE001
            result = None
    if result is None:
        # and if that fails, too, find an android folder looking at path on the sys.path
        # warning: only works for apps installed under /data, not adopted storage etc.
        pattern = re.compile(r"/data/(data|user/\d+)/(.+)/files")
        for path in sys.path:
            if pattern.match(path):
                result = path.split("/files")[0]
                break
        else:
            result = None
    if result is None:
        # one last try: find an android folder looking at path on the sys.path taking adopted storage paths into
        # account
        pattern = re.compile(r"/mnt/expand/[a-fA-F0-9-]{36}/(data|user/\d+)/(.+)/files")
        for path in sys.path:
            if pattern.match(path):
                result = path.split("/files")[0]
                break
        else:
            result = None
    return result


def _android_folder() -> str | None:  # noqa: C901
    """:return: base folder for the Android OS or None if it cannot be found"""
    result: str | None = None
    # type checker isn't happy with our "import android", just don't do this when type checking see
    # https://stackoverflow.com/a/61394121
    if not TYPE_CHECKING:
        try:
            # First try to get a path to android app using python4android (if available)...
            from android import mActivity  # noqa: PLC0415

            context = cast("android.content.Context", mActivity.getApplicationContext())  # noqa: F821
            result = context.getFilesDir().getParentFile().getAbsolutePath()
        except Exception:  # noqa: BLE001
            result = None
    if result is None:
        try:
            # ...and fall back to using plain pyjnius, if python4android isn't available or doesn't deliver any useful
            # result...
            from jnius import autoclass  # noqa: PLC0415

            context = autoclass("android.content.Context")
            result = context.getFilesDir().getParentFile().getAbsolutePath()
        except Exception:  # noqa: BLE001
            result = None
    if result is None:
        # and if that fails, too, find an android folder looking at path on the sys.path
        # warning: only works for apps installed under /data, not adopted storage etc.
        pattern = re.compile(r"/data/(data|user/\d+)/(.+)/files")
        for path in sys.path:
            if pattern.match(path):
                result = path.split("/files")[0]
                break
        else:
            result = None
    if result is None:
        # one last try: find an android folder looking at path on the sys.path taking adopted storage paths into
        # account
        pattern = re.compile(r"/mnt/expand/[a-fA-F0-9-]{36}/(data|user/\d+)/(.+)/files")
        for path in sys.path:
            if pattern.match(path):
                result = path.split("/files")[0]
                break
        else:
            result = None
    return result

