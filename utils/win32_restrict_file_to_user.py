
def win32_restrict_file_to_user(fname: str) -> None:
    """Secure a windows file to read-only access for the user.
    Follows guidance from win32 library creator:
    http://timgolden.me.uk/python/win32_how_do_i/add-security-to-a-file.html

    This method should be executed against an already generated file which
    has no secrets written to it yet.

    Parameters
    ----------

    fname : unicode
        The path to the file to secure
    """
    try:
        import win32api  # noqa: PLC0415
    except ImportError:
        return _win32_restrict_file_to_user_ctypes(fname)

    import ntsecuritycon as con  # noqa: PLC0415
    import win32security  # noqa: PLC0415

    # everyone, _domain, _type = win32security.LookupAccountName("", "Everyone")
    admins = win32security.CreateWellKnownSid(win32security.WinBuiltinAdministratorsSid)
    user, _domain, _type = win32security.LookupAccountName(
        "", win32api.GetUserNameEx(win32api.NameSamCompatible)
    )

    sd = win32security.GetFileSecurity(fname, win32security.DACL_SECURITY_INFORMATION)

    dacl = win32security.ACL()
    # dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, everyone)
    dacl.AddAccessAllowedAce(
        win32security.ACL_REVISION,
        con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE | con.DELETE,
        user,
    )
    dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, admins)

    sd.SetSecurityDescriptorDacl(1, dacl, 0)
    win32security.SetFileSecurity(fname, win32security.DACL_SECURITY_INFORMATION, sd)
    return None

