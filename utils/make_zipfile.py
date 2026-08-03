import os

def make_zipfile(
    zip_filename: StrPathT,
    base_dir,
    verbose: bool = False,
    compress=True,
    mode: _ZipFileMode = 'w',
) -> StrPathT:
    """Create a zip file from all the files under 'base_dir'.  The output
    zip file will be named 'base_dir' + ".zip".  Uses either the "zipfile"
    Python module (if available) or the InfoZIP "zip" utility (if installed
    and found on the default search path).  If neither tool is available,
    raises DistutilsExecError.  Returns the name of the output zip file.
    """
    import zipfile

    mkpath(os.path.dirname(zip_filename))  # type: ignore[arg-type] # python/mypy#18075
    log.info("creating '%s' and adding '%s' to it", zip_filename, base_dir)

    def visit(z, dirname, names):
        for name in names:
            path = os.path.normpath(os.path.join(dirname, name))
            if os.path.isfile(path):
                p = path[len(base_dir) + 1 :]
                z.write(path, p)
                log.debug("adding '%s'", p)

    compression = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED
    z = zipfile.ZipFile(zip_filename, mode, compression=compression)
    for dirname, dirs, files in sorted_walk(base_dir):
        visit(z, dirname, files)
    z.close()
    return zip_filename


def make_zipfile(
    base_name: str,
    base_dir: str | os.PathLike[str],
    verbose: bool = False,
) -> str:
    """Create a zip file from all the files under 'base_dir'.

    The output zip file will be named 'base_name' + ".zip".  Uses either the
    "zipfile" Python module (if available) or the InfoZIP "zip" utility
    (if installed and found on the default search path).  If neither tool is
    available, raises DistutilsExecError.  Returns the name of the output zip
    file.
    """
    zip_filename = base_name + ".zip"
    mkpath(os.path.dirname(zip_filename))

    # If zipfile module is not available, try spawning an external
    # 'zip' command.
    if zipfile is None:
        if verbose:
            zipoptions = "-r"
        else:
            zipoptions = "-rq"

        try:
            spawn(["zip", zipoptions, zip_filename, base_dir])
        except DistutilsExecError:
            # XXX really should distinguish between "couldn't find
            # external 'zip' command" and "zip failed".
            raise DistutilsExecError(
                f"unable to create zip file '{zip_filename}': "
                "could neither import the 'zipfile' module nor "
                "find a standalone zip utility"
            )

    else:
        log.info("creating '%s' and adding '%s' to it", zip_filename, base_dir)

        try:
            zip = zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_DEFLATED)
        except RuntimeError:
            zip = zipfile.ZipFile(zip_filename, "w", compression=zipfile.ZIP_STORED)

        with zip:
            if base_dir != os.curdir:
                path = os.path.normpath(os.path.join(base_dir, ''))
                zip.write(path, path)
                log.info("adding '%s'", path)
            for dirpath, dirnames, filenames in os.walk(base_dir):
                for name in dirnames:
                    path = os.path.normpath(os.path.join(dirpath, name, ''))
                    zip.write(path, path)
                    log.info("adding '%s'", path)
                for name in filenames:
                    path = os.path.normpath(os.path.join(dirpath, name))
                    if os.path.isfile(path):
                        zip.write(path, path)
                        log.info("adding '%s'", path)

    return zip_filename

