import os

def fudge_dir_mtimes(dir: str, delta: int) -> None:
    # Skip linker outputs. Pushing them back combines with write_file's
    # +1 sec bump on .c files to make .c always newer than .so, forcing
    # an unconditional rebuild that would mask Extension.depends bugs.
    # See setuptools/_distutils/command/build_ext.py:`build_extension`.
    for dirpath, _, filenames in os.walk(dir):
        for name in filenames:
            if name.endswith((".so", ".pyd", ".o", ".obj")):
                continue
            path = os.path.join(dirpath, name)
            new_mtime = os.stat(path).st_mtime + delta
            os.utime(path, times=(new_mtime, new_mtime))

