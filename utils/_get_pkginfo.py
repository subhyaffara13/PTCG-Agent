
def _get_pkginfo(dist: Distribution):
    with io.StringIO() as fp:
        dist.metadata.write_pkg_file(fp)
        return fp.getvalue()

