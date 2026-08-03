import os

def write_pkg_info(self, base_dir):
    """Write the PKG-INFO file into the release tree."""
    temp = ""
    final = os.path.join(base_dir, 'PKG-INFO')
    try:
        # Use a temporary file while writing to avoid race conditions
        # (e.g. `importlib.metadata` reading `.egg-info/PKG-INFO`):
        with NamedTemporaryFile("w", encoding="utf-8", dir=base_dir, delete=False) as f:
            temp = f.name
            self.write_pkg_file(f)
        permissions = stat.S_IMODE(os.lstat(temp).st_mode)
        os.chmod(temp, permissions | stat.S_IRGRP | stat.S_IROTH)
        os.replace(temp, final)  # atomic operation.
    finally:
        if temp and os.path.exists(temp):
            os.remove(temp)


def write_pkg_info(cmd, basename, filename) -> None:
    log.info("writing %s", filename)
    metadata = cmd.distribution.metadata
    metadata.version, oldver = cmd.egg_version, metadata.version
    metadata.name, oldname = cmd.egg_name, metadata.name

    try:
        metadata.write_pkg_info(cmd.egg_info)
    finally:
        metadata.name, metadata.version = oldname, oldver

    safe = getattr(cmd.distribution, 'zip_safe', None)

    bdist_egg.write_safety_flag(cmd.egg_info, safe)

