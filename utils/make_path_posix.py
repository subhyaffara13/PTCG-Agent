import os

def make_path_posix(path):
    """Make path generic and absolute for current OS"""
    if not isinstance(path, str):
        if isinstance(path, (list, set, tuple)):
            return type(path)(make_path_posix(p) for p in path)
        else:
            path = stringify_path(path)
            if not isinstance(path, str):
                raise TypeError(f"could not convert {path!r} to string")
    if os.sep == "/":
        # Native posix
        if path.startswith("/"):
            # most common fast case for posix
            return path
        elif path.startswith("~"):
            return osp.expanduser(path)
        elif path.startswith("./"):
            path = path[2:]
        elif path == ".":
            path = ""
        return f"{os.getcwd()}/{path}"
    else:
        # NT handling
        if path[0:1] == "/" and path[2:3] == ":":
            # path is like "/c:/local/path"
            path = path[1:]
        if path[1:2] == ":":
            # windows full path like "C:\\local\\path"
            if len(path) <= 3:
                # nt root (something like c:/)
                return path[0] + ":/"
            path = path.replace("\\", "/")
            return path
        elif path[0:1] == "~":
            return make_path_posix(osp.expanduser(path))
        elif path.startswith(("\\\\", "//")):
            # windows UNC/DFS-style paths
            return "//" + path[2:].replace("\\", "/")
        elif path.startswith(("\\", "/")):
            # windows relative path with root
            path = path.replace("\\", "/")
            return f"{osp.splitdrive(os.getcwd())[0]}{path}"
        else:
            path = path.replace("\\", "/")
            if path.startswith("./"):
                path = path[2:]
            elif path == ".":
                path = ""
            return f"{make_path_posix(os.getcwd())}/{path}"

