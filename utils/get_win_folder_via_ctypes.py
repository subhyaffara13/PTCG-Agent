
def get_win_folder_via_ctypes(csidl_name: str) -> str:
    """Get folder via :func:`SHGetKnownFolderPath`.

    See https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-shgetknownfolderpath.

    """
    if sys.platform != "win32":  # only needed for type checker to know that this code runs only on Windows
        raise NotImplementedError
    from ctypes import HRESULT, POINTER, Structure, WinDLL, byref, create_unicode_buffer, wintypes  # noqa: PLC0415

    class _GUID(Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8),
        ]

    ole32 = WinDLL("ole32")
    ole32.CLSIDFromString.restype = HRESULT
    ole32.CLSIDFromString.argtypes = [wintypes.LPCOLESTR, POINTER(_GUID)]
    ole32.CoTaskMemFree.restype = None
    ole32.CoTaskMemFree.argtypes = [wintypes.LPVOID]

    shell32 = WinDLL("shell32")
    shell32.SHGetKnownFolderPath.restype = HRESULT
    shell32.SHGetKnownFolderPath.argtypes = [POINTER(_GUID), wintypes.DWORD, wintypes.HANDLE, POINTER(wintypes.LPWSTR)]

    kernel32 = WinDLL("kernel32")
    kernel32.GetShortPathNameW.restype = wintypes.DWORD
    kernel32.GetShortPathNameW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR, wintypes.DWORD]

    folder_guid = _KNOWN_FOLDER_GUIDS.get(csidl_name)
    if folder_guid is None:
        msg = f"Unknown CSIDL name: {csidl_name}"
        raise ValueError(msg)

    guid = _GUID()
    ole32.CLSIDFromString(folder_guid, byref(guid))

    path_ptr = wintypes.LPWSTR()
    shell32.SHGetKnownFolderPath(byref(guid), _KF_FLAG_DONT_VERIFY, None, byref(path_ptr))
    result = path_ptr.value
    ole32.CoTaskMemFree(path_ptr)

    if result is None:
        msg = f"SHGetKnownFolderPath returned NULL for {csidl_name}"
        raise ValueError(msg)

    if any(ord(c) > 255 for c in result):  # noqa: PLR2004
        buf = create_unicode_buffer(1024)
        if kernel32.GetShortPathNameW(result, buf, 1024):
            result = buf.value

    return result


def get_win_folder_via_ctypes(csidl_name: str) -> str:
    """Get folder with ctypes."""
    # There is no 'CSIDL_DOWNLOADS'.
    # Use 'CSIDL_PROFILE' (40) and append the default folder 'Downloads' instead.
    # https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid

    import ctypes  # noqa: PLC0415

    csidl_const = {
        "CSIDL_APPDATA": 26,
        "CSIDL_COMMON_APPDATA": 35,
        "CSIDL_LOCAL_APPDATA": 28,
        "CSIDL_PERSONAL": 5,
        "CSIDL_MYPICTURES": 39,
        "CSIDL_MYVIDEO": 14,
        "CSIDL_MYMUSIC": 13,
        "CSIDL_DOWNLOADS": 40,
        "CSIDL_DESKTOPDIRECTORY": 16,
    }.get(csidl_name)
    if csidl_const is None:
        msg = f"Unknown CSIDL name: {csidl_name}"
        raise ValueError(msg)

    buf = ctypes.create_unicode_buffer(1024)
    windll = getattr(ctypes, "windll")  # noqa: B009 # using getattr to avoid false positive with mypy type checker
    windll.shell32.SHGetFolderPathW(None, csidl_const, None, 0, buf)

    # Downgrade to short path name if it has high-bit chars.
    if any(ord(c) > 255 for c in buf):  # noqa: PLR2004
        buf2 = ctypes.create_unicode_buffer(1024)
        if windll.kernel32.GetShortPathNameW(buf.value, buf2, 1024):
            buf = buf2

    if csidl_name == "CSIDL_DOWNLOADS":
        return os.path.join(buf.value, "Downloads")  # noqa: PTH118

    return buf.value


def get_win_folder_via_ctypes(csidl_name: str) -> str:
    """Get folder with ctypes."""
    # There is no 'CSIDL_DOWNLOADS'.
    # Use 'CSIDL_PROFILE' (40) and append the default folder 'Downloads' instead.
    # https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid

    import ctypes  # noqa: PLC0415

    csidl_const = {
        "CSIDL_APPDATA": 26,
        "CSIDL_COMMON_APPDATA": 35,
        "CSIDL_LOCAL_APPDATA": 28,
        "CSIDL_PERSONAL": 5,
        "CSIDL_MYPICTURES": 39,
        "CSIDL_MYVIDEO": 14,
        "CSIDL_MYMUSIC": 13,
        "CSIDL_DOWNLOADS": 40,
        "CSIDL_DESKTOPDIRECTORY": 16,
    }.get(csidl_name)
    if csidl_const is None:
        msg = f"Unknown CSIDL name: {csidl_name}"
        raise ValueError(msg)

    buf = ctypes.create_unicode_buffer(1024)
    windll = getattr(ctypes, "windll")  # noqa: B009 # using getattr to avoid false positive with mypy type checker
    windll.shell32.SHGetFolderPathW(None, csidl_const, None, 0, buf)

    # Downgrade to short path name if it has high-bit chars.
    if any(ord(c) > 255 for c in buf):  # noqa: PLR2004
        buf2 = ctypes.create_unicode_buffer(1024)
        if windll.kernel32.GetShortPathNameW(buf.value, buf2, 1024):
            buf = buf2

    if csidl_name == "CSIDL_DOWNLOADS":
        return os.path.join(buf.value, "Downloads")  # noqa: PTH118

    return buf.value

