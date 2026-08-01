
def copystat(src, dest):
    """Copy permission,  last modification time,
    last access time, and flags from src to dst."""
    import shutil

    shutil.copystat(str(src), str(dest))

