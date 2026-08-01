
def _mlsd2(ftp, path="."):
    """
    Fall back to using `dir` instead of `mlsd` if not supported.

    This parses a Linux style `ls -l` response to `dir`, but the response may
    be platform dependent.

    Parameters
    ----------
    ftp: ftplib.FTP
    path: str
        Expects to be given path, but defaults to ".".
    """
    lines = []
    minfo = []
    ftp.dir(path, lines.append)
    for line in lines:
        split_line = line.split(maxsplit=8)
        if len(split_line) < 9:
            continue
        name = split_line[8]
        unix_mode = split_line[0]
        if unix_mode[0] == "l" and " -> " in name:
            # Symbolic link: "<name> -> <target>"; keep only the link name.
            name = name.split(" -> ", 1)[0]
        this = (
            name,
            {
                "modify": " ".join(split_line[5:8]),
                "unix.owner": split_line[2],
                "unix.group": split_line[3],
                "unix.mode": unix_mode,
                "size": split_line[4],
            },
        )
        if this[1]["unix.mode"][0] == "d":
            this[1]["type"] = "dir"
        else:
            this[1]["type"] = "file"
        minfo.append(this)
    return minfo

